import discord
from constant.config import bot

@bot.tree.command(name='jrule', description='Explain the rules of Just One in Thai.')
async def jshow_rules(interaction: discord.Interaction):
  rules = (
      "**ข้อห้ามของเกม Just One:**\n"
      "- ห้ามใบ้คำด้วย **คำที่มีอยู่ในคำนั้น** เช่น ได้คำว่า **รถ Tesla** ห้ามมีคำว่า **รถ** อยู่ในคำใบ้\n"
      "- ห้ามใบ้คำด้วย **คำผวน** เช่น ได้คำว่า **เชียงใหม่** ห้ามใบ้คำว่า **ชายเหมี่ยง** อยู่ในคำใบ้\n"
      "- ห้ามใบ้คำด้วย **การแปลเป็นภาษาอื่น** เช่น ได้คำว่า **ตลาดนัดปรเมษฐ์** ห้ามใบ้คำว่า **Market** อยู่ในคำใบ้\n"
  )
  await interaction.response.send_message(rules)