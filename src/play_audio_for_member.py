import random
from play_audio import play_audio

RANDOMNESS = random.choice([True,False,False,False,False]) # 20% chance to play audio 

async def play_audio_for_member(voice_client, member_id):
  if member_id == 1114079769022173194:
      await play_audio(voice_client, 'sounds/hi-mon.m4a')
      return

  if RANDOMNESS:
      await play_audio(voice_client, 'sounds/hi.m4a')