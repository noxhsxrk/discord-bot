import csv
import discord
import os
from constant.config import bot, AUTHORIZED_USER_ID

class PointsView(discord.ui.View):
  def __init__(self, questions, current_question_index, header):
      super().__init__()
      self.questions = questions
      self.current_question_index = current_question_index
      self.header = header

      for name in header[1:]:
          button = discord.ui.Button(label=name, custom_id=name)
          button.callback = self.create_callback(name)
          self.add_item(button)

  def create_callback(self, name):
      async def callback(interaction: discord.Interaction):
          index = self.header.index(name)
          self.questions[self.current_question_index][index] = '1'
          with open('ScoreBoard.csv', 'w', newline='', encoding='utf-8') as csvfile:
              writer = csv.writer(csvfile)
              writer.writerows(self.questions)
          await interaction.response.send_message(f"เพิ่มแต้มให้กับ: **{name}** 1 แต้ม เย่ๆ")
      return callback

@bot.tree.command(name='haddpoint', description='Add points to specified players.')
async def add_points_view(interaction: discord.Interaction):
  if interaction.user.id != AUTHORIZED_USER_ID:
      await interaction.response.send_message("You are not authorized to add a point.", ephemeral=True)
      return
  
  if not os.path.exists('ScoreBoard.csv'):
      await interaction.response.send_message("No active session.", ephemeral=True)
      return

  with open('ScoreBoard.csv', 'r', newline='', encoding='utf-8') as csvfile:
      reader = csv.reader(csvfile)
      questions = list(reader)

  current_question_index = None
  for i, row in enumerate(reversed(questions)):
      if row[0] != "Result" and row[0] != "_":
          current_question_index = len(questions) - 1 - i
          break

  if current_question_index is None:
      await interaction.response.send_message("No active question found to add points.", ephemeral=True)
      return

  header = questions[0]

  view = PointsView(questions, current_question_index, header)
  await interaction.response.send_message("Click a button to add a point to a player:", view=view, ephemeral=True)