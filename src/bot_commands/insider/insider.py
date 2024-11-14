import discord
import random
from constant.config import bot, active_lumi_members, lumi_members, name_mapping
import ollama
import os
import asyncio

def get_session_file_path(user_id, insider_name, word, status="active"):
    return f"insider_session_{user_id}_{insider_name}_{word}_{status}.log"

class WordSelectionView(discord.ui.View):
    def __init__(self, words, regenerate_callback):
        super().__init__()
        self.selected_word = None
        self.regenerate_callback = regenerate_callback

        for word in words:
            truncated_word = word[:80]
            button = discord.ui.Button(label=truncated_word, custom_id=truncated_word)
            button.callback = self.create_callback(truncated_word)
            self.add_item(button)

        regenerate_button = discord.ui.Button(
            label="สุ่มคำศัพท์ใหม่", 
            custom_id="regenerate", 
            style=discord.ButtonStyle.danger
        )
        regenerate_button.callback = self.regenerate_callback
        self.add_item(regenerate_button)

    def create_callback(self, word):
        async def callback(interaction: discord.Interaction):
            self.selected_word = word
            self.stop()
            await interaction.followup.send(f"Word '{word}' selected.")
        return callback

@bot.tree.command(name='insider', description='Start a new Insider game session.')
async def start_insider(interaction: discord.Interaction, without: str = None, show_insider: bool = True, minutes: int = 10):
    global active_lumi_members, session_starter_id

    await interaction.response.defer(ephemeral=True)

    excluded_names = set(name.strip() for name in without.split(',')) if without else set()
    active_lumi_members[:] = [member for member in lumi_members if member['name'] not in excluded_names]
    print(active_lumi_members)
    
    active_sessions = [f for f in os.listdir() if f.startswith('insider_session_') and f.endswith('_active.log')]
    if active_sessions:
        await interaction.followup.send("An Insider session is already active. Please end it before starting a new one.", ephemeral=True)
        return

    if not active_lumi_members:
        await interaction.followup.send("No active members available to start the game.", ephemeral=True)
        return

    selected_member = random.choice(active_lumi_members)
    selected_member_name = name_mapping.get(selected_member['name'], selected_member['name'])

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
    words = response['response'].strip().split(',')

    async def regenerate_words(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        response = ollama.generate(model='llama3.2', prompt=prompt)
        words = response['response'].strip().split(',')
        view = WordSelectionView(words, regenerate_callback=regenerate_words)
        
        if interaction.response.is_done():
            await interaction.followup.send("Please pick a word for the game:", view=view, ephemeral=True)
        else:
            await interaction.response.edit_message(content="Please pick a word for the game:", view=view)

    view = WordSelectionView(words, regenerate_callback=regenerate_words)
    await interaction.followup.send("Please pick a word for the game:", view=view, ephemeral=True)

    await view.wait()

    if view.selected_word is None:
        await interaction.followup.send("You took too long to respond. Please try again.", ephemeral=True)
        return

    word = view.selected_word

    session_file_path = get_session_file_path(interaction.user.id, selected_member_name, word)

    with open(session_file_path, 'w') as session_file:
        session_file.write(f"Session started by {interaction.user.id}")

    user = await bot.fetch_user(selected_member['id'])
    await user.send(f"คุณถูกเลือกให้เป็น Insider. เกมเริ่มด้วยคำว่า {word} ")

    if show_insider:
        await interaction.followup.send(f"{selected_member_name} ถูกเลือกให้เป็น Insider. เกมเริ่มด้วยคำว่า {word} ", ephemeral=True)
    else:
        await interaction.followup.send(f"เกมเริ่มด้วยคำว่า {word} ", ephemeral=True)

    embed = discord.Embed(title="Insider Game Countdown", description=f"Time remaining: {minutes} minutes", color=discord.Color.blue())
    countdown_message = await interaction.channel.send(embed=embed)

    total_seconds = minutes * 60
    for remaining in range(total_seconds, 0, -1):
        await asyncio.sleep(1)
        remaining_minutes, remaining_seconds = divmod(remaining, 60)
        embed.description = f"Time remaining: {remaining_minutes} minutes {remaining_seconds} seconds"
        await countdown_message.edit(embed=embed)

    session_files = [f for f in os.listdir() if f.startswith("insider_session_") and f.endswith("_active.log")]
    for session_file in session_files:
        new_name = session_file.replace("_active.log", "_deactive.log")
        os.rename(session_file, new_name)

    await interaction.channel.send("หมดเวลาแล้วครับ", ephemeral=True)