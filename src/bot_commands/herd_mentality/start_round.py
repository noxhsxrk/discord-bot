import csv
import os
import glob
import discord
from constant.config import AUTHORIZED_USER_ID, bot, name_mapping, submitted_users, active_lumi_members

@bot.tree.command(name='hquiz', description='Start a new round with a question.')
async def start_round(interaction: discord.Interaction, question: str):
  if interaction.user.id != AUTHORIZED_USER_ID:
      await interaction.response.send_message("You are not authorized to start a new round.", ephemeral=True)
      return

  if not os.path.exists('ScoreBoard.csv'):
      await interaction.response.send_message("No active session found. Please start a session with /hm.", ephemeral=True)
      return

  active_answer_boards = [f for f in glob.glob('AnswerBoard_*.csv') if '_Inactive' not in f]
  if active_answer_boards:
      await interaction.response.send_message("An active round is already in progress. Please end it before starting a new one.", ephemeral=True)
      return

  submitted_users.clear()

  with open('ScoreBoard.csv', 'a', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow([question] + ['' for _ in active_lumi_members])

  with open(f'AnswerBoard_{question}.csv', 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['player-name', 'answer'])
      for member in active_lumi_members:
          thai_name = name_mapping.get(member['name'], member['name'])
          writer.writerow([thai_name, ''])

  await interaction.response.send_message(f"เริ่มเกม!! คำถามคือ : **{question}**")