import os
import random
import asyncio
import discord
import ollama
from constant.config import bot, members_names
from .file_utils import (
    get_session_file_path, log_insider_selection,
    get_words_from_file, get_used_words, write_used_word
)
from .views import WordSelectionView, CountdownView
from .constants import INSIDER_DIRECTORY, WORDS_FILE, USED_WORD_FILE, MIN_AVAILABLE_WORDS
import colorama
from colorama import Fore
from tabulate import tabulate
from discord.ui import View, Button

colorama.init(autoreset=True)

async def start_insider(interaction: discord.Interaction, without: bool = False, hide_insider: bool = True, minutes: int = 1, custom_word: str = None, use_ai: bool = False):
    global session_starter_id

    if not interaction.response.is_done():
        await interaction.response.defer(ephemeral=True)

    excluded = set()
    
    async def get_active_members():
        channel = interaction.channel
        if isinstance(channel, discord.TextChannel):
            members = await channel.fetch_members().flatten()
        elif isinstance(channel, discord.VoiceChannel):
            members = channel.members
        else:
            return []

        return [
            {'id': member.id, 'name': member.name}
            for member in members
            if member.name not in excluded
        ]
    
    user_name = next((member['name'] for member in await get_active_members() if member['id'] == interaction.user.id), None)
    if user_name:
        excluded.add(user_name)

    class ExclusionView(View):
        def __init__(self, members):
            super().__init__()
            for member in members:
                member_name = next((m['name'] for m in members_names if m['id'] == member['id']), member['name'])
                button = Button(label=member_name, custom_id=str(member['id']))
                button.callback = self.on_button_click
                self.add_item(button)

            confirm_button = Button(label="Confirm", style=discord.ButtonStyle.green)
            confirm_button.callback = self.confirm
            self.add_item(confirm_button)

        async def on_button_click(self, interaction: discord.Interaction):
            member_name = interaction.data['custom_id']
            
            excluded.add(member_name)
            await interaction.response.send_message(f"{member_name} has been excluded.", ephemeral=True)

        async def confirm(self, interaction: discord.Interaction):
            await interaction.response.send_message("Exclusion confirmed.", ephemeral=True)
            self.stop()

    if without:
        active_members = await get_active_members()
        if not active_members:
            await interaction.followup.send("ไม่มีสมาชิกที่ใช้งานอยู่เพื่อเริ่มเกม", ephemeral=True)
            return

        view = ExclusionView(active_members)
        await interaction.followup.send("Select members to exclude:", view=view, ephemeral=True)
        await view.wait()

    def get_words():
        if use_ai:
            return generate_words_with_ollama()
        else:
            return get_words_from_file_system()

    def get_words_from_file_system():
        all_words = get_words_from_file(WORDS_FILE)
        used_words = get_used_words(os.path.join(INSIDER_DIRECTORY, USED_WORD_FILE))
        available_words = list(set(all_words) - used_words)
        if len(available_words) < MIN_AVAILABLE_WORDS:
            return None, "Not enough unused words available. Please reset the used words or add more words."
        return random.sample(available_words, 10), None

    def generate_words_with_ollama():
        prompt = (
            "Generate 10 Thai nouns in the Thai language. If they are romanized, convert them to Thai script. "
            "Separate each word with a comma, without spaces. The words can be:\n"
            "- Extremely common, everyday objects or items\n"
            "- Common items but slightly more specific\n"
            "- Moderately specific items or concepts\n"
            "- Specialized or less common items\n"
            "- Rare, technical, or highly specific items\n"
            "- Well-known characters from popular movies or anime\n"
            "- Famous tourist destinations, especially in Thailand\n"
            "- Specific names of food or other items\n"
            "- Anything on Earth or beyond, within this universe\n\n"
            "The words should be suitable for a group game where one person guesses them through yes/no questions, "
            "like in the Insider board game.\n\n"
            "Provide only the words, with no additional explanation or special characters except commas."
        )
        response = ollama.generate(model='llama3.2', prompt=prompt)
        return response['response'].strip().split(','), None

    def create_session_file(selected_member_name, word):
        session_file_path = get_session_file_path(interaction.user.id, selected_member_name, word)
        with open(session_file_path, 'w') as session_file:
            session_file.write(f"Session started by {interaction.user.id}")

    def send_insider_message(user, word):
        return user.send(f"คุณถูกเลือกให้เป็น Insider. เกมเริ่มด้วยคำว่า {word} ")

    def send_game_start_message(selected_member_name, word):
        message = f"เกมเริ่มด้วยคำว่า {word} " if hide_insider else f"{selected_member_name} ถูกเลือกให้เป็น Insider. เกมเริ่มด้วยคำว่า {word} "
        return interaction.followup.send(message, ephemeral=True)

    def update_session_files():
        session_files = [f for f in os.listdir() if f.startswith("insider_session_") and f.endswith("_active.log")]
        for session_file in session_files:
            new_name = session_file.replace("_active.log", "_deactive.log")
            os.rename(session_file, new_name)

    async def handle_word_selection(words):
        view = WordSelectionView(words, regenerate_callback=regenerate_words)
        await interaction.followup.send("กรุณาเลือกคำสำหรับเกม:", view=view, ephemeral=True)
        await view.wait()

        if view.selected_word is None:
            await interaction.followup.send("คุณใช้เวลานานเกินไป กรุณาลองใหม่อีกครั้ง", ephemeral=True)
            return None

        return view.selected_word

    async def regenerate_words(interaction: discord.Interaction):
        words, error_message = get_words()
        if error_message:
            await interaction.followup.send(error_message, ephemeral=True)
            return

        word = await handle_word_selection(words)
        if word and not use_ai:
            write_used_word(os.path.join(INSIDER_DIRECTORY, USED_WORD_FILE), word)

        return word

    active_members = await get_active_members()
    if not active_members:
        await interaction.followup.send("ไม่มีสมาชิกที่ใช้งานอยู่เพื่อเริ่มเกม", ephemeral=True)
        return

    active_sessions = [f for f in os.listdir() if f.startswith('insider_session_') and f.endswith('_active.log')]
    if active_sessions:
        await interaction.followup.send("มีการเริ่มเกม Insider อยู่แล้ว กรุณาจบเกมก่อนเริ่มใหม่", ephemeral=True)
        return

    def get_member_name(member_id):
        for member in members_names:
            if member['id'] == member_id:
                return member['name']
        return None
    
    active_members = [member for member in active_members if member['name'] not in excluded]
    
    if active_members:
        selected_member = random.choice(active_members)
    else:
        selected_member = None  

    if selected_member is None:
        await interaction.followup.send("ไม่มีสมาชิกที่ใช้งานอยู่เพื่อเริ่มเกม", ephemeral=True)
        return

    selected_member_name = get_member_name(selected_member['id']) or selected_member['name']

    word = custom_word or await regenerate_words(interaction)
    if not word:
        return

    create_session_file(selected_member_name, word)
    user = await bot.fetch_user(selected_member['id'])
    await send_insider_message(user, word)
    await send_game_start_message(selected_member_name, word)

    embed = discord.Embed(title="การนับถอยหลังเกม Insider", description=f"เวลาที่เหลือ: {minutes} นาที", color=discord.Color.blue())
    countdown_message = await interaction.channel.send(embed=embed)

    view = CountdownView()
    await countdown_message.edit(view=view)

    total_seconds = minutes * 60
    for remaining in range(total_seconds, -1, -1):
        if view.stop_timer:
            break
        await asyncio.sleep(1)
        remaining_minutes, remaining_seconds = divmod(remaining, 60)
        embed.description = f"เวลาที่เหลือ: {remaining_minutes} นาที {remaining_seconds} วินาที"
        await countdown_message.edit(embed=embed)
        log_game_state(word, selected_member_name, hide_insider, f"{remaining_minutes} นาที {remaining_seconds} วินาที")

    update_session_files()
    log_insider_selection(selected_member_name, word)
    log_game_state(word, selected_member_name, hide_insider, "0 นาที 0 วินาที")

    if not view.stop_timer:
        await interaction.channel.send("หมดเวลาแล้วครับ")
    else:
        await interaction.channel.send("จบเกมแล้วครับ")

def log_game_state(word, insider_name, hide_insider, time_left):
    display_insider_name = "******" if hide_insider else insider_name

    data = [
        ["Guessing Word", word],
        ["Insider", display_insider_name],
        ["Time Left", time_left]
    ]

    table = tabulate(data, headers=["", ""], tablefmt="grid")

    print(Fore.BLUE + table)

    log_game_state.last_table = table