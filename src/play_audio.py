import discord

async def play_audio(voice_client, audio_path):
  if not voice_client.is_playing():
      audio_source = discord.FFmpegPCMAudio(audio_path)
      voice_client.play(audio_source)