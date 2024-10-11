import discord
from discord.ext import commands
from constant.config import lumi_members, questions, bot, name_mapping

@bot.tree.command(name='question', description='Send a question to all members except the specified member.')
async def question(interaction: discord.Interaction, name: str, q_number: str, number: str):
  question_text = questions.get(q_number, {}).get(number, "ไม่พบคำถาม")

  excluded_member = next((member for member in lumi_members if member['name'].lower() == name.lower()), None)

  if not excluded_member:
      await interaction.response.send_message(f"Member '{name}' not found.", ephemeral=True)
      return

  await interaction.response.defer(ephemeral=True)

  for member in lumi_members:
      if member['name'].lower() != name.lower():
          user = await bot.fetch_user(member['id'])
          try:
              await user.send(question_text)
          except discord.Forbidden:
              print(f"ส่งข้อความไปหา {name_mapping[member['name']]} (ID: {member['id']}) ไม่ได้")

  await interaction.followup.send(f"ส่งคำถามไปหาทุกคน ยกเว้น '{name}' เรียบร้อยแล้ว", ephemeral=True)