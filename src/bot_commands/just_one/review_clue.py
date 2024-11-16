import discord
from .game_logic import current_session, players
from constant.config import bot, lumi_members

import csv

@bot.tree.command(name='jreview-clue', description='Send clues to players for review.')
async def jreview_command(interaction: discord.Interaction):
    if current_session["guesser"] is None:
        await interaction.response.send_message("No active session. Please start a session first.", ephemeral=True)
        return

    with open('src/bot_commands/just_one/clues.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        clues = list(reader)

    clues_message = "\n".join([f"{next((member['name'] for member in lumi_members if member['id'] == name), name)}: {clue}" for name, clue in clues])

    for member in players:  
        if member['name'] != current_session["guesser"]:
            user = await bot.fetch_user(member['id'])
            await user.send(f"Review the clues:\n{clues_message}")

    await interaction.response.send_message("Clues sent for review.", ephemeral=True)