import discord
from constant.config import bot
import os
from .constants import INSIDER_DIRECTORY

@bot.tree.command(name='end-insider', description='End the current Insider game session.')
async def end_insider(interaction: discord.Interaction):
    session_files = [f for f in os.listdir(INSIDER_DIRECTORY) if f.startswith("insider_session_") and f.endswith("_active.log")]
    
    if not session_files:
        await interaction.response.send_message("No active Insider session to end.", ephemeral=True)
        return

    with open(os.path.join(INSIDER_DIRECTORY, session_files[0]), 'r') as f:
        content = f.read()
        starter_id = int(content.split()[-1])
        if interaction.user.id != starter_id:
            await interaction.response.send_message("Only the user who started the session can end it.", ephemeral=True)
            return

    for session_file in session_files:
        new_name = session_file.replace("_active.log", "_deactive.log")
        os.rename(os.path.join(INSIDER_DIRECTORY, session_file), os.path.join(INSIDER_DIRECTORY, new_name))

    await interaction.response.send_message("The Insider session has been ended.", ephemeral=True)
