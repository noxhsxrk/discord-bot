import discord
from constant.config import bot, current_session, log_game_state
import os   

@bot.tree.command(name='jend', description='End the current Just One game session.')
async def jend_command(interaction: discord.Interaction):
    current_session["active_player"] = None
    current_session["clues"] = {}
    
    if os.path.exists('clues.csv'):
        os.remove('clues.csv')
    
    log_game_state("Ended", current_session["clues"], current_session["active_player"])
    await interaction.response.send_message("Session ended. Ready for a new game.", ephemeral=True)