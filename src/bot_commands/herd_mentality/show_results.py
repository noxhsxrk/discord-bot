import csv
import os
import discord
from constant.config import bot, AUTHORIZED_USER_ID
from PIL import Image, ImageDraw, ImageFont
import cairosvg
import io

def read_cow_holder_from_file(file_path='cow_holder.txt'):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def svg_to_png(svg_file, size=(20, 20)):
    png_data = cairosvg.svg2png(url=svg_file, output_width=size[0], output_height=size[1])
    return Image.open(io.BytesIO(png_data))

def generate_result_image(questions):
  max_first_col_width = max(len(row[0]) for row in questions) * 8
  num_columns = len(questions[0])
  num_rows = len(questions)
  
  cell_widths = [max_first_col_width] + [100] * (num_columns - 1)
  cell_height = 40
  width = sum(cell_widths)
  height = cell_height * num_rows
  background_color = (255, 255, 255)
  line_color = (0, 0, 0)
  text_color = (0, 0, 0)
  green_color = (0, 128, 0)
  red_color = (255, 0, 0)
  cow_holder_color = (255, 105, 180)

  cow_image = svg_to_png('assets/images/cow.svg', size=(20, 20))

  image = Image.new('RGB', (width, height), background_color)
  draw = ImageDraw.Draw(image)

  try:
      font = ImageFont.truetype("THSarabunNew.ttf", 20)
  except IOError:
      font = ImageFont.load_default()

  x_offset = 0
  for cell_width in cell_widths:
      draw.line([(x_offset, 0), (x_offset, height)], fill=line_color)
      x_offset += cell_width

  for i in range(num_rows + 1):
      y = i * cell_height
      draw.line([(0, y), (width, y)], fill=line_color)

  result_row = questions[-1]
  max_score = max(int(score) for score in result_row[1:] if score.isdigit())

  pink_cow_holder = read_cow_holder_from_file()

  for row_index, row in enumerate(questions):
      x_offset = 0
      for col_index, cell in enumerate(row):
          y_offset = row_index * cell_height + 10

          if row_index == len(questions) - 1:
              if cell.isdigit() and int(cell) == max_score and col_index != 0:
                  draw.text((x_offset + 10, y_offset), str(cell), fill=red_color, font=font)
              else:
                  draw.text((x_offset + 10, y_offset), str(cell), fill=text_color, font=font)
          elif cell == '1':
              draw.text((x_offset + 10, y_offset), str(cell), fill=green_color, font=font)
          else:
              if row_index == 0 and questions[0][col_index] == pink_cow_holder:
                  draw.text((x_offset + 10, y_offset), str(cell), fill=cow_holder_color, font=font)
                  image.paste(cow_image, (x_offset + 30, y_offset), cow_image)
              else:
                  draw.text((x_offset + 10, y_offset), str(cell), fill=text_color, font=font)

          x_offset += cell_widths[col_index]

  image.save('result.png')

@bot.tree.command(name='hresult', description='Show current results and end the round.')
async def show_results(interaction: discord.Interaction):

    try:
        if interaction.user.id != AUTHORIZED_USER_ID:
            await interaction.response.send_message("You are not authorized to show results.", ephemeral=True)
            return

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
        await interaction.followup.send(f"An error occurred: {str(e)}")
