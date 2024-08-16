import discord

async def connect_bot_to_voice_channel(interaction, voice_channel):
  voice_client = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
  
  if voice_client:
      await voice_client.disconnect()
  
  await voice_channel.connect()
  await interaction.response.send_message(f"Connected to {voice_channel.name}", ephemeral=True)