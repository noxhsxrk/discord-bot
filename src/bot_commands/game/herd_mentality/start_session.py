import csv
import os
import discord
from constant.config import AUTHORIZED_USER_ID, bot, name_mapping

@bot.tree.command(name='herdmentality', description='Start a new Herd Mentality session.')
async def start_session(interaction: discord.Interaction, without: str = None):
  if interaction.user.id != AUTHORIZED_USER_ID:
      await interaction.response.send_message("You are not authorized to start a new session.", ephemeral=True)
      return

  if os.path.exists('ScoreBoard.csv'):
      await interaction.response.send_message("A session is already active. Please end it with /he before starting a new one.", ephemeral=True)
      return

  excluded_names = set(name.strip() for name in without.split(',')) if without else set()

  # Fetch and filter members directly from the channel
  channel_members = [member for member in interaction.channel.members if member.display_name not in excluded_names]

  with open('ScoreBoard.csv', 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      header = ['_'] + [member.display_name for member in channel_members]
      writer.writerow(header)
      writer.writerow(['Result'] + ['' for _ in channel_members])

  await interaction.response.send_message("**New Herd Mentality session started!**")