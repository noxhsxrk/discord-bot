import csv
import os
import discord
from constant.config import bot, name_mapping
from PIL import Image, ImageDraw, ImageFont

@bot.tree.command(name='hr', description='Show current results and end the round.')
async def show_results(interaction: discord.Interaction):
    with open('ScoreBoard.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        questions = list(reader)

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

    generate_result_image(scores)

    await interaction.response.send_message(file=discord.File('result.png'), ephemeral=True)

    current_question = None
    for row in reversed(questions[:-1]):
        if row[0] != "Result" and row[0] != "_":
            current_question = row[0]
            break

    if current_question:
        answer_board_filename = f'AnswerBoard_{current_question}.csv'
        if os.path.exists(answer_board_filename):
            os.rename(answer_board_filename, f'AnswerBoard_{current_question}_Inactive.csv')

def generate_result_image(scores):
    width, height = 400, 50 + 30 * len(scores)
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("THSarabunNew.ttf", 20)
    except IOError:
        print("Font not found. Using default font.")
        font = ImageFont.load_default()

    y_offset = 10
    for name, score in scores.items():
        thai_name = name_mapping.get(name, name)
        text = f"{thai_name}: {score}"
        draw.text((10, y_offset), text, fill=text_color, font=font)
        y_offset += 30

    image.save('result.png')