import discord
from .game_logic import current_session, log_game_state, submitted_players
from constant.config import bot, members_names
import csv  

@bot.tree.command(name='ja', description='Submit a clue word.')
async def ja_command(interaction: discord.Interaction, clue: str):
    if current_session["guesser"] is None:
        await interaction.response.send_message("No active session. Please start a session first.", ephemeral=True)
        return

    submitter_name = next((member['name'] for member in members_names if member['id'] == interaction.user.id), interaction.user.name)
    
    if submitter_name == current_session["guesser"]:
        await interaction.response.send_message("The active player cannot submit a clue.", ephemeral=True)
        return

    if submitter_name in submitted_players:
        await interaction.response.send_message("You have already submitted a clue.", ephemeral=True)
        return

    submitted_players.add(submitter_name)

    current_session["clues"][submitter_name] = clue
    log_game_state("Started", current_session["clues"], current_session["guesser"])

    with open('src/bot_commands/game/just_one/clues.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([submitter_name, clue])

    channel = interaction.channel
    message_id = current_session.get("embed_message_id")
    if message_id:
        message = await channel.fetch_message(message_id)
        embed = message.embeds[0]
        for i, field in enumerate(embed.fields):
            if field.name == submitter_name:
                embed.set_field_at(i, name=field.name, value="🟢 submitted", inline=False)
                break
        await message.edit(embed=embed)

    all_submitted = all(
        member['name'] in current_session["clues"] or member['name'] == current_session["guesser"]
        for member in members_names
    )

    if all_submitted:
        log_game_state("Reviewing", current_session["clues"], current_session["guesser"])

    await interaction.response.send_message(f"Clue '{clue}' submitted.", ephemeral=True)