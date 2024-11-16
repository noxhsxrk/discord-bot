from collections import defaultdict
from datetime import datetime, timedelta, timezone
import json
import os

from dotenv import load_dotenv
import openai
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
token = os.getenv('TOKEN')
guild_id = int(os.getenv('GUILD_ID'))
openai.api_key = os.getenv('OPENAI_API_KEY')
AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID'))
lumi_members = json.loads(os.getenv('LUMI_MEMBERS'))
members_names = json.loads(os.getenv('MEMBERS_NAMES'))

active_lumi_members = []
conversation_history = defaultdict(list)

def load_questions():
  with open('src/constant/questions.json', 'r', encoding='utf-8') as f:
      return json.load(f)

questions = load_questions()

def convert_to_utc(time_str):
  time_obj = datetime.strptime(time_str, "%H:%M:%S GMT+7")
  time_obj = time_obj.replace(tzinfo=timezone(timedelta(hours=7)))
  return time_obj.astimezone(timezone.utc).time()

submitted_users = set()

name_mapping = {
    "pr": "แพรว",
    "k": "ขวัญ",
    "fern": "เฟิร์น",
    "mark": "มาร์ค",
    "pla": "ปลา",
    "beer": "เบียร์",
    "faii": "ฝ้าย",
    "o": "โอ",
    "n": "อ้น",
}
