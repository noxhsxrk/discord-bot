import csv
import os
import discord
from constant.config import bot
from PIL import Image, ImageDraw, ImageFont

def generate_result_image(questions):
  num_columns = len(questions[0])
  num_rows = len(questions)
  cell_width = 100
  cell_height = 40
  width = cell_width * num_columns
  height = cell_height * num_rows
  background_color = (255, 255, 255)
  line_color = (0, 0, 0)
  text_color = (0, 0, 0)
  green_color = (0, 128, 0)
  red_color = (255, 0, 0)

  image = Image.new('RGB', (width, height), background_color)
  draw = ImageDraw.Draw(image)

  try:
      font = ImageFont.truetype("THSarabunNew.ttf", 20)
  except IOError:
      print("Font not found. Using default font.")
      font = ImageFont.load_default()

  for i in range(num_columns + 1):
      x = i * cell_width
      draw.line([(x, 0), (x, height)], fill=line_color)

  for i in range(num_rows + 1):
      y = i * cell_height
      draw.line([(0, y), (width, y)], fill=line_color)

  result_row = questions[-1]
  max_score = max(int(score) for score in result_row[1:] if score.isdigit())

  for row_index, row in enumerate(questions):
      for col_index, cell in enumerate(row):
          x_offset = col_index * cell_width + 10
          y_offset = row_index * cell_height + 10

          if row_index == len(questions) - 1:
              if cell.isdigit() and int(cell) == max_score and col_index != 0:
                  draw.text((x_offset, y_offset), str(cell), fill=red_color, font=font)
              else:
                  draw.text((x_offset, y_offset), str(cell), fill=text_color, font=font)
          elif cell == '1':
              draw.text((x_offset, y_offset), str(cell), fill=green_color, font=font)
          else:
              draw.text((x_offset, y_offset), str(cell), fill=text_color, font=font)

  image.save('result.png')

@bot.tree.command(name='hresult', description='Show current results and end the round.')
async def show_results(interaction: discord.Interaction):
  try:
      await interaction.response.defer()

      with open('ScoreBoard.csv', 'r', newline='', encoding='utf-8') as csvfile:
          reader = csv.reader(csvfile)
          questions = list(reader)

      for row in questions:
          for i in range(1, len(row)):
              if row[i] == '':
                  row[i] = '0'

      scores = {name: 0 for name in questions[0][1:]}
      for row in questions[1:]:
          if row[0] != "Result":
              for i, score in enumerate(row[1:], start=1):
                  if score == '1':
                      scores[questions[0][i]] += 1

      result_row = ['Result'] + [str(scores[name]) for name in questions[0][1:]]
      
      questions = [row for row in questions if row[0] != "Result"]
      questions.append(result_row)

      with open('ScoreBoard.csv', 'w', newline='', encoding='utf-8') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerows(questions)

      generate_result_image(questions)

      await interaction.followup.send(file=discord.File('result.png'))

      current_question = None
      for row in reversed(questions[:-1]):
          if row[0] != "Result" and row[0] != "_":
              current_question = row[0]
              break

      if current_question:
          answer_board_filename = f'AnswerBoard_{current_question}.csv'
          if os.path.exists(answer_board_filename):
              os.rename(answer_board_filename, f'AnswerBoard_{current_question}_Inactive.csv')

  except Exception as e:
      # Use follow-up message to send error details
      await interaction.followup.send(f"An error occurred: {str(e)}")