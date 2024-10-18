import csv
import os
import discord
from constant.config import AUTHORIZED_USER_ID, lumi_members, bot, name_mapping, active_lumi_members

@bot.tree.command(name='herdmentality', description='Start a new Herd Mentality session.')
async def start_session(interaction: discord.Interaction, without: str = None):
  global active_lumi_members

  if interaction.user.id != AUTHORIZED_USER_ID:
      await interaction.response.send_message("You are not authorized to start a new session.", ephemeral=True)
      return

  if os.path.exists('ScoreBoard.csv'):
      await interaction.response.send_message("A session is already active. Please end it with /he before starting a new one.", ephemeral=True)
      return

  excluded_names = set(name.strip() for name in without.split(',')) if without else set()

  active_lumi_members[:] = [member for member in lumi_members if member['name'] not in excluded_names]

  with open('ScoreBoard.csv', 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      header = ['_'] + [name_mapping[member['name']] for member in active_lumi_members]
      writer.writerow(header)
      writer.writerow(['Result'] + ['' for _ in active_lumi_members])

  await interaction.response.send_message("**New Herd Mentality session started!**")