import discord

from play_audio import play_audio

async def connect_bot_to_voice_channel(interaction, voice_channel): 
  voice_client = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)

  if voice_client and voice_client.channel != voice_channel:
      await voice_client.disconnect()

  if not voice_client or voice_client.channel != voice_channel:
      voice_client = await voice_channel.connect() 
      await play_audio(voice_client, 'sounds/hi.m4a')
      await interaction.response.send_message(f"พี่โอ๊ตมาห้อง {voice_channel.name} แล้ว", ephemeral=True)
  else:
      await interaction.response.send_message(f"พี่โอ๊ตก็อยู่ห้อง {voice_channel.name} อยู่แล้วนะ", ephemeral=True)