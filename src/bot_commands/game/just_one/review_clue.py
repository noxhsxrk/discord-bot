import discord
from .game_logic import current_session, players
from constant.config import bot, lumi_members

import csv
import os

@bot.tree.command(name='jreview-clue', description='Send clues to players for review.')
async def jreview_command(interaction: discord.Interaction):
    if current_session["guesser"] is None:
        await interaction.response.send_message("No active session. Please start a session first.", ephemeral=True)
        return

    file_path = 'src/bot_commands/game/just_one/clues.csv'
    if not os.path.exists(file_path):
        await interaction.response.send_message("Clues file not found. Please check the file path.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        clues = list(reader)

    clues_message = "=================\n" + "\n".join(
        [f"{next((member['name'] for member in lumi_members if member['id'] == name), name)}: {clue}" for name, clue in clues]
    ) + "\n================="

    for member in players:  
        if member['name'] != current_session["guesser"]:
            user = await bot.fetch_user(member['id'])
            try:
                await user.send(f"Review the clues:\n{clues_message}")
            except discord.errors.Forbidden:
                await interaction.followup.send(
                    f"Could not send message to {member['name']}. They might have DMs disabled or have blocked the bot.",
                    ephemeral=True
                )

    await interaction.followup.send("Clues sent for review.", ephemeral=True)