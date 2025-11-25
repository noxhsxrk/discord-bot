import discord
import json
import os
from discord import app_commands
from constant.config import members_names, C_DATA_FILE, MAX_SUBMISSIONS

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

@app_commands.command(name="c", description="Submit a text")
async def c_command(interaction: discord.Interaction, text: str):
    user_id = interaction.user.id
    
    # members_names is a list of dicts: [{'id': 123, 'name': 'Name'}, ...]
    # Create a mapping for easy lookup
    authorized_users = {}
    if isinstance(members_names, list):
        for member in members_names:
            if isinstance(member, dict) and 'id' in member and 'name' in member:
                authorized_users[str(member['id'])] = member['name']
    
    if str(user_id) not in authorized_users:
        await interaction.response.send_message("คุณไม่มีสิทธิ์ใช้คำสั่งนี้", ephemeral=True)
        return

    user_name = authorized_users[str(user_id)]

    data = load_data()
    
    # Migration: Convert string values to list
    migrated = False
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = [value]
            migrated = True
    
    if migrated:
        save_data(data)

    # Check if user has reached submission limit
    user_submissions = data.get(user_name, [])
    if len(user_submissions) >= MAX_SUBMISSIONS:
        await interaction.response.send_message(f"คุณส่งข้อความครบ {MAX_SUBMISSIONS} ครั้งแล้ว ไม่สามารถส่งเพิ่มได้", ephemeral=True)
        return

    # Save data as list
    if user_name not in data:
        data[user_name] = []
    data[user_name].append(text)
    
    try:
        save_data(data)
    except Exception as e:
        await interaction.response.send_message(f"เกิดข้อผิดพลาดในการบันทึก: {e}", ephemeral=True)
        return

    await interaction.response.send_message(f"บันทึกข้อความเรียบร้อย: {text}", ephemeral=True)
