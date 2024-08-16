import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

custom_messages = {
  1075642752173363250: "สวัสดีคร้าบพี่แพรววววว",
  100357927685299409: "หวัดดีค้าบพี่แคป",
  1158406612189466634: "อ่าวหวัดดีบ่าวเคนน",
  943486622199078933: "หวัดดีค้าบฟลุ๊ค",
  1247481192803074069: "หวัดดีเท่าที่จำเป็นครับพี่ขวัญ",
  833904793004015639: "ดีฮะหน่องเฟิร์น",
  1244849737979396121: "หวัดดีครับน้องปริญ",
  612569701368856581: "หวัดดีไอ้อ้น",
  1003506434522226698: "สวัสดีครับพี่เฟรมมมมมม",
  915653082526937110: "สวัสดีครับเฟิร์ส",
  993185809320652811: "หวัดดีครับน้องบาสส",
  846709460146585610: "ไอ้มาร์ค เป็นไง สบายดีมั้ย",
  326697982890213378: "ไอ้มาร์ค เป็นไง สบายดีมั้ย",
  245948348241149953: "ขอบคุณพี่ไมท์คร้าบบบบบบบบ",
  927765122636738571: "สวัสดีครับพี่ปลาาาาาา",
  250997223255572480: "สวัสดีครับพี่ธัญจิโร่",
  257396927077941248: "สวัสดีครับน้องปลื้มมมมม",
  317304806647791619: "ไอ้เบียร์~~~~ ฮัลโหลลลลล"
}

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  await bot.tree.sync() 
  print("Commands synced.")

@bot.tree.command(name='oat', description='Summon the bot to your current voice channel')
async def oat(interaction: discord.Interaction):
  if interaction.user.voice and interaction.user.voice.channel:
      voice_channel = interaction.user.voice.channel
      voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
      if voice_client:
          # Disconnect from the current voice channel
          await voice_client.disconnect()
      

      await voice_channel.connect()
      await interaction.response.send_message(f"Connected to {voice_channel.name}", ephemeral=True)
  else:
      await interaction.response.send_message("You need to be in a voice channel to use this command.", ephemeral=True)

@bot.event
async def on_voice_state_update(member, before, after):
  if member.id != bot.user.id:
      if after.channel and member.id in custom_messages:
          message = custom_messages[member.id]
          voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
          if voice_client and voice_client.channel:
              text_channel_id = voice_client.channel.id
              text_channel = bot.get_channel(text_channel_id)
              if text_channel:
                  await text_channel.send(f"{message}")
              else:
                  print("Text channel not found.")
          else:
              print("Bot is not connected to any voice channel in this guild.")

bot.run(token)