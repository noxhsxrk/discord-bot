import csv
import os
import discord
from constant.config import bot, name_mapping

@bot.tree.command(name='hp', description='Add points to specified players.')
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
    for name in name_list:
        thai_name = name_mapping.get(name.strip())
        if thai_name in header:
            index = header.index(thai_name)
            questions[current_question_index][index] = '1'

    with open('ScoreBoard.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(questions)

    await interaction.response.send_message(f"Points added for: {', '.join(name_list)}", ephemeral=True)