import discord
from discord import app_commands

@app_commands.command(name="cex", description="Show game rules and commands")
async def cex_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="กติกาและคำสั่ง (Game Rules & Commands)",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="คำสั่งทั่วไป (General Commands)",
        value="คำสั่งต่างๆ ที่จะให้คน submit มา",
        inline=False
    )

    embed.add_field(
        name="1. หมุนซ้าย (Rotate Left)",
        value="จานที่อยู่ตรงหน้าเราจะย้ายไปหาคนทางซ้าย",
        inline=False
    )
    embed.add_field(
        name="2. หมุนขวา (Rotate Right)",
        value="จานที่อยู่ตรงหน้าเราจะย้ายไปหาคนทางขวา",
        inline=False
    )
    embed.add_field(
        name="3. สลับ A & B (A กับ B เป็นชื่อผุ้เล่น)",
        value="ผู้เล่น 2 คนเพื่อสลับจานกัน",
        inline=False
    )
    embed.add_field(
        name="4. อยู่เฉยๆ (Stay Still)",
        value="จานทุกใบอยู่ที่เดิม",
        inline=False
    )
    embed.add_field(
        name="5. สลับกับซ้าย (Swap w/ Left)",
        value="คนที่มีจาน แมลงสาบ จะสลับจานกับคนทาง **ซ้ายมือ** ของตัวเองทันที",
        inline=False
    )
    embed.add_field(
        name="6. สลับกับขวา (Swap w/ Right)",
        value="คนที่มีจานแมลงสาบ จะสลับจานกับคนทาง **ขวามือ** ของตัวเองทันที",
        inline=False
    )
    embed.add_field(
        name="7. สลับกับคนตรงข้าม (Swap Opposite)",
        value="คนที่มีจาน แมลงสาบ จะสลับจานกับคนที่นั่ง **ตรงข้าม**\n*กรณีคนเล่นจำนวนคี่*: ระบบจะสุ่มเลือกระหว่างคนตรงข้ามทางซ้ายหรือทางขวา (50/50) เพื่อความยุติธรรม",
        inline=False
    )

    await interaction.response.send_message(embed=embed)
