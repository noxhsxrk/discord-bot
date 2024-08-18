from play_audio_for_member import play_audio_for_member
from messages import custom_messages
import time
from collections import defaultdict

last_message_time = defaultdict(lambda: 0)

COOLDOWN_PERIOD = 60

async def handle_user_join_channel(voice_client, channel, member):
  if not voice_client or voice_client.channel != channel:
      print("Bot is not connected to the same voice channel.")
      return

  current_time = time.time()
  last_time = last_message_time[member.id]

  message = custom_messages.get(member.id)
  if message:
      if current_time - last_time >= COOLDOWN_PERIOD:
          text_channel = voice_client.guild.get_channel(voice_client.channel.id)
          if text_channel:
              await text_channel.send(message)
              last_message_time[member.id] = current_time
          else:
              print("Text channel not found.")

  await play_audio_for_member(voice_client, member.id)