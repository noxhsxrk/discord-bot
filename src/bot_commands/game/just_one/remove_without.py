import discord
from discord.ui import View, Button
from constant.config import bot

def read_without_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def remove_from_without_file(file_path, names_to_remove):
    current_names = read_without_file(file_path)
    updated_names = [name for name in current_names if name not in names_to_remove]
    with open(file_path, 'w', encoding='utf-8') as file:
        for name in updated_names:
            file.write(f"{name}\n")

@bot.tree.command(name='jremove-without', description='Remove members from the exclusion list.')
async def jremove_without_command(interaction: discord.Interaction):
    excluded_members = read_without_file('src/bot_commands/game/just_one/without.csv')
    member_buttons = []
    selected_members = set()

    for member_name in excluded_members:
        button = Button(label=member_name, style=discord.ButtonStyle.danger)
        
        async def button_callback(interaction: discord.Interaction, member_name=member_name):
            if member_name in selected_members:
                selected_members.remove(member_name)
                await interaction.response.send_message(f"Unmarked {member_name} for removal.", ephemeral=True)
            else:
                selected_members.add(member_name)
                await interaction.response.send_message(f"Marked {member_name} for removal.", ephemeral=True)
        
        button.callback = button_callback
        member_buttons.append(button)

    class RemoveButtonView(View):
        def __init__(self):
            super().__init__()
            for button in member_buttons:
                self.add_item(button)
            confirm_button = Button(label="Confirm Removal", style=discord.ButtonStyle.success)
            confirm_button.callback = self.confirm_callback
            self.add_item(confirm_button)

        async def confirm_callback(self, interaction: discord.Interaction):
            remove_from_without_file('src/bot_commands/game/just_one/without.csv', selected_members)
            await interaction.response.send_message(f"Removed members: {', '.join(selected_members)}", ephemeral=True)

    await interaction.response.send_message("Select members to remove and confirm:", view=RemoveButtonView(), ephemeral=True)
