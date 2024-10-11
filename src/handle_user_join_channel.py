import json
import os
from get_openai_response import get_openai_response
from play_audio_for_member import play_audio_for_member
import time
from collections import defaultdict
from constant.config import members_names

last_message_time = defaultdict(lambda: 0)
COOLDOWN_PERIOD = 3600

pre_generated_messages = {}

async def generate_message_for_member(member_id, name):
    prompt = f"ทักทาย {name} อย่างเป็นกันเอง สั้นๆ ไม่ต้องเป็นทางการ มีกวนๆ บ้าง ไม่ต้องถามกลับ และต้องไม่มีคำว่า แซว หรือ กวน อยู่ในข้อความ"
    message = await get_openai_response(prompt, 75)
    pre_generated_messages[member_id] = message

async def pre_generate_messages():
    for member in members_names:
        await generate_message_for_member(member["id"], member["name"])

async def handle_user_join_channel(voice_client, channel, member):
  if not voice_client or voice_client.channel != channel:
      print("Bot is not connected to the same voice channel.")
      return

  current_time = time.time()
  last_time = last_message_time[member.id]

  if current_time - last_time >= COOLDOWN_PERIOD:
      message = pre_generated_messages.get(member.id, "สวัสดีครับ")
      message_with_mention = f"<@{member.id}> {message}"

      text_channel = voice_client.guild.get_channel(voice_client.channel.id)
      if text_channel:
          async with text_channel.typing():
              await text_channel.send(message_with_mention)
          last_message_time[member.id] = current_time

          member_info = next((m for m in members_names if m["id"] == member.id), None)
          if member_info:
              await generate_message_for_member(member.id, member_info["name"])
      else:
          print("Text channel not found.")

  await play_audio_for_member(voice_client, member.id)