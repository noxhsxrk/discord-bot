import discord
from constant.config import bot, lumi_members
from .game_logic import current_session, log_game_state

import csv

@bot.tree.command(name='jshow-clue', description='Show clues in the channel.')
async def jshow_clue_command(interaction: discord.Interaction):
    if current_session["guesser"] is None:
        await interaction.response.send_message("No active session. Please start a session first.", ephemeral=True)
        return

    with open('src/bot_commands/just_one/clues.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        clues = list(reader)

    clues_message = "\n".join([f"{next((member['name'] for member in lumi_members if member['id'] == name), name)}: {clue}" for name, clue in clues])

    await interaction.channel.send(f"Here are the clues:\n{clues_message}")
    await interaction.response.send_message("Clues have been sent to the channel.", ephemeral=True)
    
    log_game_state("Guessing", current_session["clues"], current_session["guesser"])
