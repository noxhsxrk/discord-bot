import discord
from discord.ui import View, Button
from constant.config import bot, members_names

selected_members = set()

def add_to_without_file(file_path, names):
    with open(file_path, 'w', encoding='utf-8') as file:
        for name in names:
            file.write(f"{name}\n")

@bot.tree.command(name='jwithout', description='Select members to exclude from the game.')
async def jwithout_command(interaction: discord.Interaction):
    channel_members = interaction.channel.members
    member_buttons = []

    for member in channel_members:
        member_name = next((m['name'] for m in members_names if m['id'] == member.id), member.name)
        button = Button(label=member_name, style=discord.ButtonStyle.primary)
        
        async def button_callback(interaction: discord.Interaction, member_name=member_name):
            if member_name in selected_members:
                selected_members.remove(member_name)
                await interaction.response.send_message(f"Removed {member_name} from exclusion list.", ephemeral=True)
            else:
                selected_members.add(member_name)
                await interaction.response.send_message(f"Added {member_name} to exclusion list.", ephemeral=True)
        
        button.callback = button_callback
        member_buttons.append(button)

    class WithoutButtonView(View):
        def __init__(self):
            super().__init__()
            for button in member_buttons:
                self.add_item(button)
            confirm_button = Button(label="Confirm", style=discord.ButtonStyle.success)
            confirm_button.callback = self.confirm_callback
            self.add_item(confirm_button)

        async def confirm_callback(self, interaction: discord.Interaction):
            add_to_without_file('src/bot_commands/game/just_one/without.csv', selected_members)
            await interaction.response.send_message(f"Excluded members: {', '.join(selected_members)}", ephemeral=True)

    await interaction.response.send_message("Select members to exclude and confirm:", view=WithoutButtonView(), ephemeral=True)