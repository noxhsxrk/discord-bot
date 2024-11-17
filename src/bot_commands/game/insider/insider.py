import discord
from constant.config import bot
from .game_logic import start_insider

@bot.tree.command(name='insider', description='Start a new Insider game session.')
async def insider_command(interaction: discord.Interaction, without: bool = False, hide_insider: bool = True, minutes: int = 1, custom_word: str = None, use_ai: bool = False):
    await start_insider(interaction, without, hide_insider, minutes, custom_word, use_ai)