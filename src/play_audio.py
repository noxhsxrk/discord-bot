import asyncio
import discord

async def play_audio(voice_client, audio_path):
  if not voice_client.is_playing():
      print(f"Playing audio: {audio_path}")
      audio_source = discord.FFmpegOpusAudio(audio_path)
      voice_client.play(audio_source)