import discord
import random
from constant.config import bot, active_lumi_members, lumi_members, name_mapping
import ollama
import os

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
async def start_insider(interaction: discord.Interaction, without: str = None, show_insider: bool = True):
    global active_lumi_members, session_starter_id

    await interaction.response.defer(ephemeral=True)

    excluded_names = set(name.strip() for name in without.split(',')) if without else set()
    active_lumi_members[:] = [member for member in lumi_members if member['name'] not in excluded_names]
    
    active_sessions = [f for f in os.listdir() if f.startswith('insider_session_') and f.endswith('_active.log')]
    if active_sessions:
        await interaction.followup.send("มีเกม Insider ที่มีการเริ่มต้นอยู่แล้ว กรุณาสิ้นสุดก่อนที่จะเริ่มเกมใหม่ โดยใช้คำสั่ง /end-insider", ephemeral=True)
        return

    if not active_lumi_members:
        await interaction.followup.send("No active members available to start the game.", ephemeral=True)
        return

    selected_member = random.choice(active_lumi_members)
    selected_member_name = name_mapping.get(selected_member['name'], selected_member['name'])

    prompt = f"Generate 10 Thai nouns separated by commas without spaces where:\n\n" \
                "Words can be Extremely common, everyday objects/items that everyone knows and uses\n" \
                "or Common items but slightly more specific\n" \
                "or Moderately specific items or concepts\n" \
                "or Specialized or less common items\n" \
                "or Rare, technical, or highly specific items\n" \
                "or Well-known characters from popular movies or anime that most people would recognize\n\n" \
                "The words should be suitable for a group game where one person needs to guess them through yes/no questions like in the Insider board game.\n\n" \
                "Just give me the words in Thai separated by commas without spaces, no other explanation. No special characters except commas."

    response = ollama.generate(model='llama3.2', prompt=prompt)
    words = response['response'].strip().split(',')

    async def regenerate_words(interaction: discord.Interaction):
        response = ollama.generate(model='llama3.2', prompt=prompt)
        words = response['response'].strip().split(',')
        view = WordSelectionView(words, regenerate_callback=regenerate_words)

        await interaction.followup.edit_message(interaction.message.id, content="เลือกคำศัพท์สำหรับเกม:", view=view)

    view = WordSelectionView(words, regenerate_callback=regenerate_words)
    await interaction.followup.send("เลือกคำศัพท์สำหรับเกม:", view=view, ephemeral=True)

    await view.wait()

    if view.selected_word is None:
        await interaction.followup.send("คุณไม่ได้เลือกคำศัพท์ในระยะเวลาที่กำหนด กรุณาลองใหม่อีกครั้ง", ephemeral=True)
        return

    word = view.selected_word

    session_file_path = get_session_file_path(interaction.user.id, selected_member_name, word)

    with open(session_file_path, 'w') as session_file:
        session_file.write(f"Session started by {interaction.user.id}")

    user = await bot.fetch_user(612569701368856581)
    await user.send(f"คุณถูกเลือกให้เป็น Insider. เกมเริ่มด้วยคำว่า {word} ")

    if show_insider:
        await interaction.followup.send(f"{selected_member_name} ถูกเลือกให้เป็น Insider. เกมเริ่มด้วยคำว่า {word} ", ephemeral=True)
    else:
        await interaction.followup.send(f"เกมเริ่มด้วยคำว่า {word} ", ephemeral=True)