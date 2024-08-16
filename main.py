import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from messages import custom_messages

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  await bot.tree.sync()
  print("Commands synced.")

@bot.tree.command(name='oat', description='Summon the bot to your current voice channel')
async def oat(interaction: discord.Interaction):
  user_voice = interaction.user.voice
  if user_voice and user_voice.channel:
      voice_channel = user_voice.channel
      voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
      
      if voice_client:
          await voice_client.disconnect()
      
      await voice_channel.connect()
      await interaction.response.send_message(f"Connected to {voice_channel.name}", ephemeral=True)
  else:
      await interaction.response.send_message("You need to be in a voice channel to use this command.", ephemeral=True)

@bot.event
async def on_voice_state_update(member, before, after):
  if member.id == bot.user.id:
      return

  if after.channel and after.channel != before.channel:
      voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
      
      if voice_client and voice_client.channel == after.channel:
          message = custom_messages.get(member.id)
          if message:
              text_channel = bot.get_channel(voice_client.channel.id)
              if text_channel:
                  await text_channel.send(message)
                  await play_audio_for_member(voice_client, member.id)
              else:
                  print("Text channel not found.")
      else:
          print("Bot is not connected to the same voice channel.")

async def play_audio_for_member(voice_client, member_id):
  if member_id == 1114079769022173194:
      if not voice_client.is_playing():
          audio_source = discord.FFmpegPCMAudio('sounds/hi-mon.mp3')
          voice_client.play(audio_source)
          return

  if random.randint(1, 6) == 1:
      if not voice_client.is_playing():
          audio_source = discord.FFmpegPCMAudio('sounds/hi.mp3')
          voice_client.play(audio_source)

bot.run(token)