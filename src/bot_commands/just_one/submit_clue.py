import discord
from .game_logic import current_session, log_game_state
from constant.config import bot, active_lumi_members
import csv  


@bot.tree.command(name='ja', description='Submit a clue word.')
async def ja_command(interaction: discord.Interaction, clue: str):
    if current_session["active_player"] is None:
        await interaction.response.send_message("No active session. Please start a session first.", ephemeral=True)
        return

    submitter_name = next((member['name'] for member in active_lumi_members if member['id'] == interaction.user.id), interaction.user.name)
    
    if submitter_name == current_session["active_player"]:
        await interaction.response.send_message("The active player cannot submit a clue.", ephemeral=True)
        return

    if submitter_name in current_session["clues"]:
        await interaction.response.send_message("You have already submitted a clue.", ephemeral=True)
        return

    current_session["clues"][submitter_name] = clue
    log_game_state("Started", current_session["clues"], current_session["active_player"])

    with open('src/bot_commands/just_one/clues.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([submitter_name, clue])

    all_submitted = all(
        member['name'] in current_session["clues"] or member['name'] == current_session["active_player"]
        for member in active_lumi_members
    )

    if all_submitted:
        log_game_state("Reviewing", current_session["clues"], current_session["active_player"])

    await interaction.response.send_message(f"Clue '{clue}' submitted.", ephemeral=True)