import csv
import os
import discord
import random
from constant.config import bot, AUTHORIZED_USER_ID

@bot.tree.command(name='hshow', description='Show answers for the current question.')
async def show_answers(interaction: discord.Interaction):
  if interaction.user.id != AUTHORIZED_USER_ID:
      await interaction.response.send_message("You are not authorized to show answers.", ephemeral=True)
      return
  
  with open('ScoreBoard.csv', 'r', newline='', encoding='utf-8') as csvfile:
      reader = csv.reader(csvfile)
      questions = list(reader)

      current_question = None
      for row in reversed(questions):
          if row[0] != "Result" and row[0] != "_":
              current_question = row[0]
              break

  if current_question is None:
      await interaction.response.send_message("No active question found. Please start a round with /hq.", ephemeral=True)
      return

  answer_board_filename = f'AnswerBoard_{current_question}.csv'

  if not os.path.exists(answer_board_filename):
      await interaction.response.send_message(f"Answer board for the question '{current_question}' not found.", ephemeral=True)
      return

  with open(answer_board_filename, 'r', newline='', encoding='utf-8') as csvfile:
      reader = csv.reader(csvfile)
      answers = list(reader)
      answers = answers[1:]

  random.shuffle(answers) 

  class AnswerView(discord.ui.View):
      def __init__(self, answers):
          super().__init__()
          self.answers = answers
          for row in self.answers[1:]:
              button = discord.ui.Button(label=row[0], custom_id=row[0])
              button.callback = self.create_callback(row[0], row[1])
              self.add_item(button)

      def create_callback(self, name, answer):
          async def callback(interaction: discord.Interaction):
              await interaction.response.send_message(f"{name} : **{answer}**")
          return callback

  view = AnswerView(answers)
  await interaction.response.send_message("Click a button to see the answer:", view=view, ephemeral=True)