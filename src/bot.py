import asyncio
from datetime import datetime, timedelta, timezone
import json
import os
import random
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import openai
from langdetect import detect

from connect_bot_schedule import connect_bot_schedule
from connect_bot_to_voice_channel import connect_bot_to_voice_channel
from get_openai_response import get_openai_response
from handle_screen_share_start import handle_screen_share_start
from handle_user_join_channel import handle_user_join_channel, pre_generate_messages

load_dotenv()
token = os.getenv('TOKEN')
guild_id = int(os.getenv('GUILD_ID')) 
openai.api_key = os.getenv('OPENAI_API_KEY') 

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

with open('src/constant/fixed_times.json', 'r') as f:
  fixed_times = json.load(f)

def convert_to_utc(time_str):
  time_obj = datetime.strptime(time_str, "%H:%M:%S GMT+7")
  time_obj = time_obj.replace(tzinfo=timezone(timedelta(hours=7)))
  return time_obj.astimezone(timezone.utc).time()

fixed_times_utc = [
  {"task_name": entry["task_name"], "time": convert_to_utc(entry["time"]), "channel": entry["channel"]}
  for entry in fixed_times
]

exception_channel_ids = list({entry["channel"] for entry in fixed_times})

activities = [
    discord.Activity(type=discord.ActivityType.watching, name="กำลังดู Infra ของ Kaidee อยู่"),
    discord.Activity(type=discord.ActivityType.watching, name="กำลังดู แก้บัค ของ Kaidee อยู่"),
    discord.Activity(type=discord.ActivityType.listening, name="กำลังฟังจี่หอย"),
    discord.Activity(type=discord.ActivityType.listening, name="กำลังฟัง Die For You"),
    discord.Activity(type=discord.ActivityType.playing, name="กำลังแอบเล่น Honkai"),
    discord.Activity(type=discord.ActivityType.playing, name="กำลังแอบเล่น เกมโป๊"),
    discord.Activity(type=discord.ActivityType.watching, name="กำลังดูหนังเว็บ 037"),
]

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  try:
      await pre_generate_messages()
      print("Pre-generated messages loaded successfully.")
      bot.tree.clear_commands(guild=discord.Object(id=guild_id))
      bot.tree.add_command(oat, guild=discord.Object(id=guild_id))
      await bot.tree.sync(guild=discord.Object(id=guild_id))
      print("Commands synced successfully.")
  except Exception as e:
      print(f"Error syncing commands: {e}")
  
  asyncio.create_task(change_activity())
  schedule_daily_task.start()

async def change_activity():
  while True:
      now = datetime.now(timezone(timedelta(hours=7)))
      start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
      end_time = now.replace(hour=18, minute=0, second=0, microsecond=0)

      if start_time <= now < end_time:
          new_activity = random.choice(activities)
          await bot.change_presence(activity=new_activity)
          print(f"Changed activity to: {new_activity.name}")
      else:
          await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="กำลังเล่นเกมโป๊"))

      await asyncio.sleep(3600)

@bot.tree.command(name='oat', description='อัญเชิญพี่โอ๊ตเข้าดิส')
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
      
@bot.tree.command(name='oat-token', description='Enter your own token')
async def oat_token(interaction: discord.Interaction):
  await interaction.response.send_message(
      "Please enter your token:", ephemeral=True
  )

  def check(m):
      return m.author == interaction.user and m.channel == interaction.channel

  try:
      msg = await bot.wait_for('message', check=check, timeout=60.0)
      user_token = msg.content

      await interaction.followup.send(f"Token received: {user_token}", ephemeral=True)

  except asyncio.TimeoutError:
      await interaction.followup.send("You took too long to respond!", ephemeral=True)

@bot.event
async def on_voice_state_update(member, before, after):
  if member.id == bot.user.id:
      return

  voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)

  if not before.self_stream and after.self_stream:
      await handle_screen_share_start(voice_client, after.channel, member)

  if after.channel and after.channel != before.channel:
      await handle_user_join_channel(voice_client, after.channel, member)

@bot.event
async def on_message(message):
  if bot.user.mentioned_in(message) and not message.author.bot:
      asyncio.create_task(handle_message_response(message))
  await bot.process_commands(message)

async def handle_message_response(message):
  async with message.channel.typing():
      response = await get_openai_response(message.content, 250, message.author.id)
      await message.channel.send(response)

@tasks.loop(hours=24)
async def schedule_daily_task():
  while True:
      now = datetime.now(timezone.utc)
      next_times = []

      for entry in fixed_times_utc:
          target_time = datetime.combine(now.date(), entry["time"], tzinfo=timezone.utc)
          if now.time() >= entry["time"]:
              target_time += timedelta(days=1)
          next_times.append((target_time, entry["channel"], entry["task_name"]))

      next_time, channel_id, task_name = min(next_times, key=lambda x: x[0])

      sleep_duration = (next_time - now).total_seconds()

      hours, remainder = divmod(sleep_duration, 3600)
      minutes, seconds = divmod(remainder, 60)

      print(f"Bot will sleep for {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds until the next scheduled task: {task_name}.")

      await asyncio.sleep(sleep_duration)

      await join_voice_channel(channel_id)

async def join_voice_channel(channel_id):
  guild = bot.get_guild(guild_id)
  if guild is None:
      print(f"Guild with ID {guild_id} not found.")
      return

  channel = guild.get_channel(channel_id)
  if channel is None:
      print(f"Channel with ID {channel_id} not found in guild {guild.name}.")
      return

  voice_client = discord.utils.get(bot.voice_clients, guild=guild)

  if voice_client and voice_client.is_connected():
      if voice_client.channel.id not in exception_channel_ids:
          await voice_client.disconnect()

  await connect_bot_schedule(bot, channel)

bot.run(token)