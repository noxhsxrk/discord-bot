import random
import discord
import asyncio
from datetime import datetime, timezone, timedelta

activities = [
    discord.Activity(type=discord.ActivityType.watching, name="กำลังดู Infra ของ Kaidee อยู่"),
    discord.Activity(type=discord.ActivityType.watching, name="กำลังดู แก้บัค ของ Kaidee อยู่"),
    discord.Activity(type=discord.ActivityType.listening, name="กำลังฟังจี่หอย"),
    discord.Activity(type=discord.ActivityType.listening, name="กำลังฟัง Die For You"),
    discord.Activity(type=discord.ActivityType.playing, name="กำลังแอบเล่น Honkai"),
    discord.Activity(type=discord.ActivityType.playing, name="กำลังแอบเล่น เกมโป๊"),
    discord.Activity(type=discord.ActivityType.watching, name="กำลังดูหนังเว็บ 037"),
]

async def change_activity(bot):
    while True:
        now = datetime.now(timezone(timedelta(hours=7)))
        start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=18, minute=0, second=0, microsecond=0)

        if start_time <= now < end_time:
            new_activity = random.choice(activities)
            await bot.change_presence(activity=new_activity)
            print(f"Changed activity to: {new_activity.name}")
        else:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="กำลังเล่นเกมโป๊"))

        await asyncio.sleep(3600)