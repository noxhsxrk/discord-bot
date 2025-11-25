import discord
import json
from discord import app_commands
from constant.config import C_DATA_FILE

def save_data(data):
    with open(C_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app_commands.command(name="cc", description="Clear all data")
async def cc_command(interaction: discord.Interaction):
    try:
        save_data({})
        await interaction.response.send_message("ลบข้อมูลทั้งหมดเรียบร้อยแล้ว", ephemeral=False)
    except Exception as e:
        await interaction.response.send_message(f"เกิดข้อผิดพลาดในการลบข้อมูล: {e}", ephemeral=True)
