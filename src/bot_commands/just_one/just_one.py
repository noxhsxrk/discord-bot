import os
import random
import discord
from discord.ui import View, Select
from .game_logic import current_session, log_game_state, players
from constant.config import bot, members_names

def get_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def get_used_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(line.strip() for line in file.readlines())
    except FileNotFoundError:
        return set()

def add_word_to_used(file_path, word):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{word}\n")

@bot.tree.command(name='just1', description='Start a new Just One game session.')
async def just1_command(interaction: discord.Interaction, without: str = None):
    if os.path.exists('src/bot_commands/just_one/clues.csv'):
        os.remove('src/bot_commands/just_one/clues.csv')
        
    if current_session["guesser"] is not None:
        await interaction.response.send_message("A session is already active. Please end it before starting a new one.", ephemeral=True)
        return

    channel_members = interaction.channel.members
    player_options = [
        discord.SelectOption(
            label=next((m['name'] for m in members_names if m['id'] == member.id), member.name),
            value=next((m['name'] for m in members_names if m['id'] == member.id), member.name),
        )
        for member in channel_members
        if member.name not in (without.split(',') if without else [])
    ]

    class PlayerSelectView(View):
        @discord.ui.select(placeholder="Choose the active player", options=player_options)
        async def select_callback(self, interaction: discord.Interaction, select: Select):
            guesser = select.values[0]
            mapped_guesser = next((member['name'] for member in members_names if member['name'] == guesser), None)
            
            if not mapped_guesser:
                await interaction.response.send_message(f"Player '{guesser}' not found.", ephemeral=True)
                return

            players[:] = [
                {
                    "id": member.id,
                    "name": next((m['name'] for m in members_names if m['id'] == member.id), member.name)
                }
                for member in channel_members
                if member.name not in (without.split(',') if without else []) and member.name != guesser
            ]
            

            words = get_words_from_file('src/constant/words.txt')
            used_words = get_used_words('src/bot_commands/just_one/used_words.txt')
            available_words = list(set(words) - used_words)

            if not available_words:
                await interaction.response.send_message("No more words available. Please reset the used words list.", ephemeral=True)
                return

            selected_word = random.choice(available_words)
            current_session["word"] = selected_word
            add_word_to_used('src/bot_commands/just_one/used_words.txt', selected_word)
            
            for member in players:
                if member['name'] != mapped_guesser:
                    user = await bot.fetch_user(member['id'])
                    await user.send(f"The word to guess is: {selected_word}")

            current_session["guesser"] = mapped_guesser
            log_game_state("Started", current_session["clues"], mapped_guesser)
            await interaction.response.send_message(f"Game started! {mapped_guesser} is the guesser.", ephemeral=True)

    await interaction.response.send_message("Select the guesser:", view=PlayerSelectView(), ephemeral=True)
