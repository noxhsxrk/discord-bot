import csv
import discord
from constant.config import bot, AUTHORIZED_USER_ID, name_mapping

def get_players_from_scoreboard(file_path='ScoreBoard.csv'):
    players = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        players = header[1:]
    return players

def write_cow_holder_to_file(player_name, file_path='cow_holder.txt'):
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write(player_name)

def read_cow_holder_from_file(file_path='cow_holder.txt'):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

@bot.tree.command(name='hcow', description='Assign the pink cow to a player in the session.')
async def assign_cow(interaction: discord.Interaction, player_name: str):

    if interaction.user.id != AUTHORIZED_USER_ID:
        await interaction.response.send_message("You are not authorized to assign the pink cow.", ephemeral=True)
        return

    players = get_players_from_scoreboard()

    thai_name = name_mapping.get(player_name)

    if thai_name is None or thai_name not in players:
        await interaction.response.send_message(f"Player '{player_name}' not found in the scoreboard.", ephemeral=True)
        return

    write_cow_holder_to_file(thai_name)

    await interaction.response.send_message(f"{thai_name} ได้รับวัวสีชมพูแล้ว!")
