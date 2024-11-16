import discord
from constant.config import bot
from .game_logic import current_session, log_game_state
import os   

@bot.tree.command(name='jend', description='End the current Just One game session.')
async def jend_command(interaction: discord.Interaction):
    current_session["active_player"] = None
    current_session["clues"] = {}
    
    if os.path.exists('src/bot_commands/just_one/clues.csv'):
        os.remove('src/bot_commands/just_one/clues.csv')
    
    log_game_state("Ended", current_session["clues"], current_session["active_player"])
    await interaction.response.send_message("Session ended. Ready for a new game.", ephemeral=True)