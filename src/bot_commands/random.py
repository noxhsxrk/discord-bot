import random
import discord
from discord.ext import commands
from constant.config import bot

@bot.tree.command(name='rp', description="Randomly select one person from the current channel.")
async def random_person(interaction: discord.Interaction):
    channel_members = [member for member in interaction.channel.members if not member.bot]
    
    if not channel_members:
        await interaction.response.send_message("No members to choose from!", ephemeral=True)
        return
    
    selected_member = random.choice(channel_members)
    
    await interaction.channel.send(f"คุณ {selected_member.mention} คือผู้ที่ถูกเลือก")