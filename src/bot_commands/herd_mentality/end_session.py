import csv
from datetime import datetime
import os
from constant.config import AUTHORIZED_USER_ID,bot
import discord

@bot.tree.command(name='he', description='End the current session.')
async def end_session(interaction: discord.Interaction):
  if interaction.user.id != AUTHORIZED_USER_ID:
      await interaction.response.send_message("You are not authorized to end a session.", ephemeral=True)
      return
  
  if not os.path.exists('ScoreBoard.csv'):
      await interaction.response.send_message("No active session to end.", ephemeral=True)
      return

  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  os.rename('ScoreBoard.csv', f'ScoreBoard_{timestamp}_Inactive.csv')
  await interaction.response.send_message("Session ended and scoreboard archived.", ephemeral=True)
