import csv
import os
import discord
from constant.config import AUTHORIZED_USER_ID, lumi_members, bot, name_mapping

@bot.tree.command(name='hm', description='Start a new Herd Mentality session.')
async def start_session(interaction: discord.Interaction):
    if interaction.user.id != AUTHORIZED_USER_ID:
        await interaction.response.send_message("You are not authorized to start a new session.", ephemeral=True)
        return

    if os.path.exists('ScoreBoard.csv'):
        await interaction.response.send_message("A session is already active. Please end it with /he before starting a new one.", ephemeral=True)
        return

    with open('ScoreBoard.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        header = ['_'] + [name_mapping[member['name']] for member in lumi_members]
        writer.writerow(header)
        writer.writerow(['Result'] + ['' for _ in lumi_members])

    await interaction.response.send_message("**New Herd Mentality session started!**")