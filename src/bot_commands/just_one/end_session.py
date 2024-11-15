import discord
from .game_logic import end_session
from constant.config import bot
import os   

@bot.tree.command(name='jend', description='End the current Just One game session.')
async def jend_command(interaction: discord.Interaction):
    end_session()
    os.remove('clues.csv')

    await interaction.response.send_message("Session ended. Ready for a new game.", ephemeral=True)