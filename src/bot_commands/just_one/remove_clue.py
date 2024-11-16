import discord
from .game_logic import current_session, log_game_state, players
from constant.config import bot
import csv

class ClueRemovalView(discord.ui.View):
    def __init__(self):
        super().__init__()
        for player in players:
            if player != current_session["guesser"]:
                if isinstance(player, dict) and 'name' in player:
                    self.add_item(discord.ui.Button(label=player['name'], custom_id=player['name']))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        name = interaction.data['custom_id']
        removed_clues = set()

        if name in current_session["clues"]:
            del current_session["clues"][name]
            removed_clues.add(name)
            await interaction.response.send_message(f"Clue from {name} removed.", ephemeral=True)
        else:
            await interaction.response.send_message(f"No clue found for {name}.", ephemeral=True)

        with open('src/bot_commands/just_one/clues.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for name, clue in current_session["clues"].items():
                writer.writerow([name, clue])

        log_game_state("Started", current_session["clues"], current_session["guesser"], removed_clues)
        return True

@bot.tree.command(name='jremove-clue', description='Remove identical clues.')
async def jremove_command(interaction: discord.Interaction):
    if current_session["guesser"] is None:
        await interaction.response.send_message("No active session. Please start a session first.", ephemeral=True)
        return

    view = ClueRemovalView()

    await interaction.response.send_message("Select a player to remove their clue:", view=view, ephemeral=True)
    