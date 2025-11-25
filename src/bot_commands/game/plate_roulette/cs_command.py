import discord
import json
import os
import random
from discord import app_commands
from constant.config import C_DATA_FILE

def load_data():
    if not os.path.exists(C_DATA_FILE):
        return {}
    try:
        with open(C_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(C_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app_commands.command(name="cs", description="Randomly select and remove a text")
async def cs_command(interaction: discord.Interaction):
    data = load_data()
    
    # Collect all available texts
    # Pool structure: [(user_name, text, index_in_list)]
    pool = []
    for user, texts in data.items():
        if isinstance(texts, list):
            for i, text in enumerate(texts):
                pool.append((user, text, i))
        elif isinstance(texts, str):
            # Handle legacy string format just in case
            pool.append((user, texts, -1))

    if not pool:
        await interaction.response.send_message("ไม่มีข้อความเหลืออยู่แล้ว", ephemeral=True)
        return

    # Randomly select one
    selected_user, selected_text, index = random.choice(pool)

    # Remove from data
    if index != -1:
        # List format
        data[selected_user].pop(index)
        # If list is empty, maybe remove user key? Or keep empty list?
        # Keeping empty list is fine.
        if not data[selected_user]:
            del data[selected_user]
    else:
        # String format
        del data[selected_user]

    try:
        save_data(data)
    except Exception as e:
        await interaction.response.send_message(f"เกิดข้อผิดพลาดในการลบข้อมูล: {e}", ephemeral=True)
        return

    # Send to channel (not ephemeral)
    await interaction.response.send_message(f"ข้อความที่ได้คือ: **{selected_text}**")
