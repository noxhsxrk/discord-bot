import csv
import os
import discord
from constant.config import AUTHORIZED_USER_ID, lumi_members, bot, name_mapping, submitted_users

@bot.tree.command(name='hq', description='Start a new round with a question.')
async def start_round(interaction: discord.Interaction, question: str):
  if interaction.user.id != AUTHORIZED_USER_ID:
      await interaction.response.send_message("You are not authorized to start a new round.", ephemeral=True)
      return

  if not os.path.exists('ScoreBoard.csv'):
      await interaction.response.send_message("No active session found. Please start a session with /hm.", ephemeral=True)
      return

  submitted_users.clear()

  with open('ScoreBoard.csv', 'a', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow([question] + ['' for _ in lumi_members])

  with open(f'AnswerBoard_{question}.csv', 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['player-name', 'answer'])
      for member in lumi_members:
          thai_name = name_mapping.get(member['name'], member['name'])
          writer.writerow([thai_name, ''])

  await interaction.response.send_message(f"Round started with question: {question}", ephemeral=True)