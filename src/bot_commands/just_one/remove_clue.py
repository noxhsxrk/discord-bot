import discord
from .game_logic import current_session, log_game_state
from constant.config import bot
import csv

@bot.tree.command(name='jremove-clue', description='Remove identical clues.')
async def jremove_command(interaction: discord.Interaction, names: str):
    if current_session["active_player"] is None:
        await interaction.response.send_message("No active session. Please start a session first.", ephemeral=True)
        return

    names_to_remove = set(names.split(','))
    current_session["clues"] = {name: clue for name, clue in current_session["clues"].items() if name not in names_to_remove}

    with open('clues.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for name, clue in current_session["clues"].items():
            writer.writerow([name, clue])

    await interaction.response.send_message(f"Removed clues from: {', '.join(names_to_remove)}", ephemeral=True)
    