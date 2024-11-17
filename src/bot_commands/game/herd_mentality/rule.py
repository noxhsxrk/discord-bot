import discord
from constant.config import bot

@bot.tree.command(name='hrule', description='Explain the rules of Herd Mentality in Thai.')
async def show_rules(interaction: discord.Interaction):
  rules = (
      "**กฎของเกม Herd Mentality:**\n"
      "- **ถ้าคำตอบของคุณตรงกับคำตอบส่วนใหญ่** คุณจะได้รับแต้ม\n"
      "- **ถ้าไม่ตรง** คุณจะไม่ได้อะไรเลย\n"
      "- **ถ้าคำตอบส่วนใหญ่เสมอกัน** ไม่มีใครได้รับแต้ม\n"
      "- **ถ้าคำตอบของคุณแตกต่างจากคนอื่น ๆ** คุณจะได้รับวัวสีชมพู\n"
      "- **ถ้าคุณมีวัวสีชมพู** คุณจะไม่สามารถชนะเกมได้ แต่ยังสามารถสะสมแต้มได้\n"
      "- **เมื่อมีผู้เล่นใหม่ที่มีคำตอบแตกต่างจากคนอื่น ๆ** ให้ส่งวัวสีชมพูให้เขา"
  )
  await interaction.response.send_message(rules)