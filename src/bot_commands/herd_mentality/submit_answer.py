import csv
import os
import discord
from constant.config import lumi_members, bot, submitted_users, name_mapping

@bot.tree.command(name='ha', description='Submit an answer for the current question.')
async def submit_answer(interaction: discord.Interaction, answer: str):
    if interaction.user.id in submitted_users:
        await interaction.response.send_message("You have already submitted an answer for this round.", ephemeral=True)
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

    user_name = None
    for member in lumi_members:
        if member['id'] == interaction.user.id:
            user_name = member['name']
            break

    if user_name is None:
        await interaction.response.send_message("Your name could not be found in the member list.", ephemeral=True)
        return

    thai_name = name_mapping.get(user_name)

    with open(answer_board_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        answers = list(reader)

    for row in answers:
        if row[0] == thai_name:
            row[1] = answer
            break

    with open(answer_board_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(answers)

    submitted_users.add(interaction.user.id)
    await interaction.response.send_message(f"Answer submitted: {answer}", ephemeral=True)