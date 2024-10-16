from datetime import datetime
import os
import glob
from constant.config import AUTHORIZED_USER_ID, bot
import discord

@bot.tree.command(name='hend', description='End the current session.')
async def end_session(interaction: discord.Interaction):
    if interaction.user.id != AUTHORIZED_USER_ID:
        await interaction.response.send_message("You are not authorized to end a session.", ephemeral=True)
        return

    if not os.path.exists('ScoreBoard.csv'):
        await interaction.response.send_message("No active session to end.", ephemeral=True)
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.rename('ScoreBoard.csv', f'ScoreBoard_{timestamp}_Inactive.csv')

    active_answer_boards = glob.glob('AnswerBoard_*.csv')
    for answer_board in active_answer_boards:
        base_name = os.path.basename(answer_board)
        new_name = f"{base_name.split('.')[0]}_{timestamp}_Inactive.csv"
        os.rename(answer_board, new_name)

    await interaction.response.send_message("Session ended and all boards archived.", ephemeral=True)