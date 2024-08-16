from play_audio_for_member import play_audio_for_member
from messages import custom_messages
import time

last_message_time = {}

COOLDOWN_PERIOD = 30

async def handle_channel_join(voice_client, channel, member):
  print(last_message_time)
  if voice_client and voice_client.channel == channel:
      current_time = time.time()
      last_time = last_message_time.get(member.id, 0)
      
      if current_time - last_time >= COOLDOWN_PERIOD:
          message = custom_messages.get(member.id)
          if message:
              text_channel = voice_client.guild.get_channel(voice_client.channel.id)
              if text_channel:
                  await text_channel.send(message)
                  await play_audio_for_member(voice_client, member.id)
                  last_message_time[member.id] = current_time
              else:
                  print("Text channel not found.")
      else:
          print(f"Cooldown active for {member.display_name}. Message not sent.")
  else:
      print("Bot is not connected to the same voice channel.")