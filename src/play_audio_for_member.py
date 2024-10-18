import random
from play_audio import play_audio

async def play_audio_for_member(voice_client, member_id):
  if member_id == 1114079769022173194:
      await play_audio(voice_client, 'assets/sounds/hi-mon.m4a')
      return
  
  if random.choice([True,False,False]):
      await play_audio(voice_client, 'assets/sounds/hi.m4a')