import csv
import discord
from constant.config import bot, name_mapping

@bot.tree.command(name='haddpoint', description='Add points to specified players.')
async def add_points(interaction: discord.Interaction, names: str):
  name_list = names.split(',')

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
  valid_names = []
  invalid_names = []

  for name in name_list:
      thai_name = name_mapping.get(name.strip())
      if thai_name in header:
          index = header.index(thai_name)
          questions[current_question_index][index] = '1'
          valid_names.append(thai_name)
      else:
          invalid_names.append(name.strip())

  with open('ScoreBoard.csv', 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerows(questions)

  if valid_names:
      await interaction.response.send_message(f"เพิ่มแต้มให้กับ: **{', '.join(valid_names)}** คนละ 1 แต้ม เย่ๆ")
  if invalid_names:
      await interaction.followup.send(f"ไม่พบสมาชิก: **{', '.join(invalid_names)}** ใน ScoreBoard", ephemeral=True)