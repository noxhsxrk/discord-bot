import asyncio
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import json
import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import openai

from activity_manager import change_activity
from connect_bot_schedule import connect_bot_schedule
from connect_bot_to_voice_channel import connect_bot_to_voice_channel
from conversation_history import check_file_age, read_from_file, write_to_file
from get_openai_response import get_openai_response, handle_chat_response
from handle_screen_share_start import handle_screen_share_start
from handle_user_join_channel import handle_user_join_channel, pre_generate_messages
from image_generator import  handle_image_request

load_dotenv()
token = os.getenv('TOKEN')
guild_id = int(os.getenv('GUILD_ID'))
openai.api_key = os.getenv('OPENAI_API_KEY')
lumi_members = json.loads(os.getenv('LUMI_MEMBERS'))

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.messages = True

conversation_history = defaultdict(list)

bot = commands.Bot(command_prefix='!', intents=intents)

def load_questions():
    with open('src/constant/questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

questions = load_questions()

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

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  try:
      await pre_generate_messages()
      print("Pre-generated messages loaded successfully.")
      bot.tree.clear_commands(guild=discord.Object(id=guild_id))
      bot.tree.add_command(oat, guild=discord.Object(id=guild_id))
      bot.tree.add_command(question, guild=discord.Object(id=guild_id))
      await bot.tree.sync(guild=discord.Object(id=guild_id))
      print("Commands synced successfully.")
  except Exception as e:
      print(f"Error syncing commands: {e}")

  asyncio.create_task(change_activity(bot))
  schedule_daily_task.start()

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

@bot.tree.command(name='question', description='เกมถามไม่ตรงคำตอบของ Lumi')
async def question(interaction: discord.Interaction, name: str, q_number: str, number: str):
  question_text = questions.get(q_number, {}).get(number, "ไม่พบคำถาม")

  excluded_member = next((member for member in lumi_members if member['name'].lower() == name.lower()), None)

  if not excluded_member:
      await interaction.response.send_message(f"Member '{name}' not found.", ephemeral=True)
      return

  await interaction.response.defer(ephemeral=True)

  for member in lumi_members:
      if member['name'].lower() != name.lower():
          user = await bot.fetch_user(member['id'])
          try:
              await user.send(question_text)
          except discord.Forbidden:
              print(f"ส่งข้อความไปหา {member['name']} (ID: {member['id']}) ไม่ได้")

  await interaction.followup.send(f"ส่งคำถามไปหาทุกคน ยกเว้น '{name}' เรียบร้อยแล้ว", ephemeral=True)

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
  if message.author.bot:
      return

  channel_id = message.channel.id

  check_file_age(channel_id)

  write_to_file(channel_id, "user", message.content)

  if bot.user.mentioned_in(message):
      content_lower = message.content.lower()
      if any(keyword in content_lower for keyword in ["สร้าง", "สร้างรูป", "ขอรูป", "รูป"]):
          await handle_image_request(bot, message, content_lower)
      else:
          async with message.channel.typing():
              conversation_history = read_from_file(channel_id)
              conversation_text = "\n".join(
                  f"{entry['role']}: {entry['content']}" for entry in conversation_history
              )

              response = await get_openai_response(conversation_text, 250, message.author.id)
              await message.reply(response)

              write_to_file(channel_id, "assistant", response)

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
