import discord
from play_audio import play_audio

async def connect_bot_schedule(bot, voice_channel):
  voice_client = discord.utils.get(bot.voice_clients, guild=voice_channel.guild)

  if voice_client and voice_client.channel == voice_channel:
      return

  if voice_client:
      await voice_client.disconnect()

  voice_client = await voice_channel.connect()

  text_channel = voice_client.guild.get_channel(voice_client.channel.id)

  await play_audio(voice_client, 'sounds/hi.m4a')

  role_id = 1273863451931836500
  role_mention = f"<@&{role_id}>"

  if voice_channel.id == 1273862909717643364:
      await text_channel.send("Checkout กันค้าบบบบบ")
  elif voice_channel.id == 1273863622753255465:
      await text_channel.send(f"มอนิ่งคร้าบบบบบ ชาวลูมิ {role_mention} มาเช็คอินกัน")