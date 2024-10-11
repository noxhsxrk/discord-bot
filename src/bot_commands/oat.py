from connect_bot_to_voice_channel import connect_bot_to_voice_channel
import discord
from discord.ext import commands
from constant.config import bot

@bot.tree.command(name="oat", description="Call P'Oat to connect to the voice channel.")
async def oat(interaction: discord.Interaction):
  user_voice = interaction.user.voice
  if user_voice and user_voice.channel:
      if interaction.channel == user_voice.channel:
          await connect_bot_to_voice_channel(interaction, user_voice.channel)
      else:
          await interaction.response.send_message(
              "ฮั่นแน่!!! ใช้คำสั่งในห้องตัวเองสิ", ephemeral=True
          )
  else:
      await interaction.response.send_message(
          "เข้าห้องมาก่อนนน ค่อยเรียก", ephemeral=True
      )