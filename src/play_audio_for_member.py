import random
from play_audio import play_audio

async def play_audio_for_member(voice_client, member_id):
  if member_id == 1114079769022173194:
      await play_audio(voice_client, 'sounds/hi-mon.mp3')
  elif random.randint(1, 6) == 1:
      await play_audio(voice_client, 'sounds/hi.mp3')