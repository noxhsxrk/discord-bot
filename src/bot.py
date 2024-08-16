import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from connect_bot_to_voice_channel import connect_bot_to_voice_channel
from handle_screen_share_start import handle_screen_share_start
from handle_channel_join import handle_channel_join

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()
    print("Commands synced.")

@bot.tree.command(name='oat', description='อัญเชิญพี่โอ๊ตเข้าดิส')
async def oat(interaction: discord.Interaction):
    user_voice = interaction.user.voice
    if user_voice and user_voice.channel:
        await connect_bot_to_voice_channel(interaction, user_voice.channel)
    else:
        await interaction.response.send_message("You need to be in a voice channel to use this command.", ephemeral=True)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id:
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)

    if not before.self_stream and after.self_stream:
        await handle_screen_share_start(voice_client, after.channel, member)

    if after.channel and after.channel != before.channel:
        await handle_channel_join(voice_client, after.channel, member)

bot.run(token)