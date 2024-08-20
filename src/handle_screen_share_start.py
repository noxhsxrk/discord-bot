import json
import os
from play_audio import play_audio
from dotenv import load_dotenv

load_dotenv()
members_names = json.loads(os.getenv('MEMBERS_NAMES'))

async def handle_screen_share_start(voice_client, channel, member):
  if not voice_client or voice_client.channel != channel:
      print("Bot is not connected to the same voice channel.")
      return

  text_channel = voice_client.guild.get_channel(voice_client.channel.id)
  if not text_channel:
      print("Text channel not found.")
      return

  await play_audio(voice_client, 'sounds/can-you-see-the-screen.m4a')

  member_info = next((m for m in members_names if m["id"] == member.id), None)
  name = member_info["name"] if member_info else member.display_name

  async with text_channel.typing():
      await text_channel.send(f"เห็นจอของ {name} กันมั้ยครับ")