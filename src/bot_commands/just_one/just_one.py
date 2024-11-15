import random
import discord
from .game_logic import start_new_session, current_session, log_game_state
from constant.config import bot, active_lumi_members, lumi_members, name_mapping

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
async def just1_command(interaction: discord.Interaction, active_player: str, without: str = None):
    print(current_session)
    if current_session["active_player"] is not None:
        await interaction.response.send_message("A session is already active. Please end it before starting a new one.", ephemeral=True)
        return

    mapped_active_player_name = name_mapping.get(active_player)
    print(mapped_active_player_name)
    if not mapped_active_player_name:
        await interaction.response.send_message(f"Player '{active_player}' not found.", ephemeral=True)
        return

    excluded_names = set(name.strip() for name in without.split(',')) if without else set()
    excluded_names.add(active_player)
    active_lumi_members[:] = [member for member in lumi_members if member['name'] not in excluded_names]

    start_new_session(mapped_active_player_name)
    log_game_state("Started", current_session["clues"], mapped_active_player_name)

    words = get_words_from_file('src/bot_commands/just_one/words.txt')
    used_words = get_used_words('src/bot_commands/just_one/used_words.txt')
    available_words = list(set(words) - used_words)

    if not available_words:
        await interaction.response.send_message("No more words available. Please reset the used words list.", ephemeral=True)
        return

    selected_word = random.choice(available_words)
    current_session["word"] = selected_word
    add_word_to_used('src/bot_commands/just_one/used_words.txt', selected_word)

    for member in active_lumi_members:
        if member['name'] != mapped_active_player_name:
            user = await bot.fetch_user(member['id'])
            await user.send(f"The word to guess is: {selected_word}")

    current_session["active_player"] = active_player
    await interaction.response.send_message(f"Game started! {mapped_active_player_name} is the active player.", ephemeral=True)
