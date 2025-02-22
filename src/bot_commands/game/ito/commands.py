import discord
from discord import app_commands
from typing import Dict, List
from .ito_game import ItoGame
from .theme_manager import ThemeManager

# Store active games and their states per channel
active_games: Dict[int, ItoGame] = {}
theme_states: Dict[int, List[str]] = {}  # Store theme choices per channel
theme_manager = ThemeManager()

class ThemeSelectView(discord.ui.View):
    def __init__(self, themes: List[str], interaction: discord.Interaction, initial_lives: int = 3, cards_per_player: int = 1):
        super().__init__(timeout=60)  # 60 seconds timeout
        self.themes = themes
        self.original_interaction = interaction
        self.initial_lives = initial_lives
        self.cards_per_player = cards_per_player
        
        # Add a button for each theme
        for i, theme in enumerate(themes):
            button = discord.ui.Button(
                label=f"Theme {i+1}",
                style=discord.ButtonStyle.primary,
                custom_id=f"theme_{i}"
            )
            button.callback = self.create_callback(theme)
            self.add_item(button)
    
    def create_callback(self, theme: str):
        async def button_callback(interaction: discord.Interaction):
            channel_id = interaction.channel_id
            
            # Mark theme as used
            theme_manager.mark_theme_as_used(theme)
            
            # Create game and set up players
            game = ItoGame(theme, self.initial_lives, self.cards_per_player)
            voice_channel = interaction.user.voice.channel
            if voice_channel:
                player_ids = [member.id for member in voice_channel.members if not member.bot]
                game.setup_players(player_ids)
                
                # Start the game immediately
                if game.start_game():
                    active_games[channel_id] = game
                    
                    # Send DMs to all players with their numbers
                    player_list = []
                    for player_id, player_state in game.players.items():
                        member = interaction.guild.get_member(player_id)
                        if member:
                            numbers_str = ", ".join(str(n) for n in player_state.numbers)
                            try:
                                await member.send(f"Your number(s) for the Ito game: {numbers_str}\nTheme: {game.theme}")
                                player_list.append(f"{player_state.color} {member.display_name}")
                            except discord.Forbidden:
                                await interaction.channel.send(f"Couldn't send DM to {member.mention}. Please enable DMs!")
                    
                    players_str = "\n".join(player_list)
                    game_instructions = (
                        f"Game started with theme: **{theme}**\n\n"
                        f"Players:\n{players_str}\n\n"
                        f"Lives: ❤️ x {game.lives}\n\n"
                        "📢 Share your clues verbally in the voice channel!\n"
                        "Once everyone has shared their clues, use /ito_submit to start selecting players in order."
                    )
                    await interaction.response.edit_message(content=game_instructions, view=None)
                else:
                    await interaction.response.edit_message(content="Failed to start the game. Need at least 2 players!", view=None)
            else:
                await interaction.response.edit_message(content="You must be in a voice channel!", view=None)
            
            # Clean up theme state
            if channel_id in theme_states:
                theme_states.pop(channel_id)
            
            # Disable all buttons
            for item in self.children:
                item.disabled = True
            
            self.stop()
            
        return button_callback
    
    async def on_timeout(self):
        # Clean up on timeout
        channel_id = self.original_interaction.channel_id
        if channel_id in theme_states:
            theme_states.pop(channel_id)
            
        # Disable all buttons
        for item in self.children:
            item.disabled = True
        
        try:
            await self.original_interaction.edit_original_response(
                content="Theme selection timed out. Start a new game with /ito_start",
                view=self
            )
        except:
            pass

class PlayerSelectView(discord.ui.View):
    def __init__(self, game: ItoGame, interaction: discord.Interaction):
        super().__init__(timeout=60)
        self.game = game
        self.original_interaction = interaction
        self.selected_user_id = None
        
        # Add dropdown for player selection
        self.player_select = discord.ui.Select(
            placeholder="Choose a player",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=interaction.guild.get_member(user_id).display_name,
                    value=str(user_id),
                    emoji=game.players[user_id].color,
                    description=f"Has {self.get_remaining_cards(user_id)} card(s) left"
                ) for user_id in game.get_unselected_players()
            ]
        )
        self.player_select.callback = self.player_selected
        self.add_item(self.player_select)
    
    def get_remaining_cards(self, user_id: int) -> int:
        """Get the number of unplayed cards for a player"""
        total_cards = len(self.game.players[user_id].numbers)
        played_cards = sum(1 for uid, _ in self.game.current_arrangement if uid == user_id)
        return total_cards - played_cards
    
    def get_unplayed_numbers(self, user_id: int) -> List[int]:
        """Get the list of unplayed numbers for a player"""
        player = self.game.players[user_id]
        played_indices = [idx for uid, idx in self.game.current_arrangement if uid == user_id]
        return [num for i, num in enumerate(player.numbers) if i not in played_indices]
    
    async def player_selected(self, interaction: discord.Interaction):
        self.selected_user_id = int(self.player_select.values[0])
        
        # Clear existing number buttons if any
        for item in self.children[:]:
            if isinstance(item, discord.ui.Button):
                self.remove_item(item)
        
        # Add buttons for remaining unplayed cards
        unplayed_numbers = self.get_unplayed_numbers(self.selected_user_id)
        for i, number in enumerate(sorted(unplayed_numbers)):
            button = discord.ui.Button(
                label=f"Card {i+1}",
                style=discord.ButtonStyle.primary,
                custom_id=f"number_{number}"
            )
            button.callback = self.create_number_callback(number)
            self.add_item(button)
        
        await interaction.response.edit_message(view=self)
    
    def create_number_callback(self, number: int):
        async def number_callback(interaction: discord.Interaction):
            if not self.selected_user_id:
                await interaction.response.send_message("Please select a player first!", ephemeral=True)
                return
            
            # Get the number from the button's custom_id
            button_number = int(interaction.data['custom_id'].split('_')[1])
            
            # Check if this number is correct for the current position
            all_numbers = []
            for player in self.game.players.values():
                all_numbers.extend(player.numbers)
            all_numbers.sort()
            
            current_position = len(self.game.current_arrangement)
            if all_numbers[current_position] == button_number:
                # Correct selection
                member = interaction.guild.get_member(self.selected_user_id)
                player = self.game.players[self.selected_user_id]
                
                # Add to arrangement
                self.game.current_arrangement.append((self.selected_user_id, player.numbers.index(button_number)))
                
                # If player has played all their numbers, mark them as selected
                player_numbers_in_arrangement = sum(1 for uid, _ in self.game.current_arrangement if uid == self.selected_user_id)
                if player_numbers_in_arrangement == len(player.numbers):
                    self.game.selected_players.add(self.selected_user_id)
                
                if len(self.game.current_arrangement) == sum(len(p.numbers) for p in self.game.players.values()):
                    # Game complete
                    next_lives = self.game.get_next_theme_lives()
                    life_change = next_lives - self.game.lives
                    life_message = ""
                    if life_change > 0:
                        life_message = f"\n🎉 Perfect round! You gained a life! Next theme will start with {next_lives} lives!"
                    
                    # Show victory message with final arrangement
                    result_message = "🎉 Congratulations! You've arranged everyone correctly!\n\nFinal arrangement:\n"
                    for i, (uid, _) in enumerate(self.game.current_arrangement):
                        player = self.game.players[uid]
                        member = interaction.guild.get_member(uid)
                        number = all_numbers[i]
                        result_message += f"{i+1}. {player.color} {member.display_name}'s {number}\n"
                    
                    # Get new themes for next round
                    themes = theme_manager.get_random_themes(3)
                    if themes:
                        theme_states[interaction.channel_id] = themes
                        theme_options = "\n".join(f"{i+1}. {theme}" for i, theme in enumerate(themes))
                        
                        embed = discord.Embed(
                            title="🎲 Next Theme Selection",
                            description=f"Choose the next theme:\n\n{theme_options}",
                            color=discord.Color.blue()
                        )
                        
                        active_games.pop(interaction.channel_id)
                        await interaction.response.edit_message(content=result_message + life_message, view=None)
                        view = ThemeSelectView(themes, interaction, next_lives, self.game.cards_per_player)
                        await interaction.channel.send(embed=embed, view=view)
                    else:
                        active_games.pop(interaction.channel_id)
                        await interaction.response.edit_message(
                            content=result_message + "\nNo more themes available! Game complete!",
                            view=None
                        )
                else:
                    # Continue game
                    await interaction.response.edit_message(
                        content=f"✅ Correct! {player.color} {member.display_name}'s {button_number} is in position {current_position + 1}!\n\n"
                               f"Lives remaining: ❤️ x {self.game.lives}\n\n"
                               f"Use /ito_submit to select the next player!",
                        view=None
                    )
            else:
                # Wrong selection
                self.game.lives -= 1
                self.game.wrong_guesses += 1
                member = interaction.guild.get_member(self.selected_user_id)
                player = self.game.players[self.selected_user_id]
                
                if self.game.lives <= 0:
                    # Game over
                    result_message = "❌ Game Over! You've run out of lives!\n\nCorrect order was:\n"
                    for i, number in enumerate(all_numbers):
                        for uid, p in self.game.players.items():
                            if number in p.numbers:
                                m = interaction.guild.get_member(uid)
                                result_message += f"{i+1}. {p.color} {m.display_name}'s {number}\n"
                                break
                    
                    active_games.pop(interaction.channel_id)
                    await interaction.response.edit_message(content=result_message, view=None)
                else:
                    await interaction.response.edit_message(
                        content=f"❌ Wrong! {player.color} {member.display_name}'s {button_number} is not in position {current_position + 1}!\n\n"
                               f"Lives remaining: ❤️ x {self.game.lives}\n\n"
                               f"Try again with /ito_submit",
                        view=None
                    )
            
            self.stop()
            
        return number_callback

@app_commands.command(name="ito_start", description="Start a new Ito game")
@app_commands.describe(cards_per_player="Number of cards per player (1 or 2)")
async def start_ito(interaction: discord.Interaction, cards_per_player: int = 1):
    channel_id = interaction.channel_id
    
    if channel_id in active_games:
        await interaction.response.send_message("A game is already in progress in this channel!")
        return
    
    # Validate cards_per_player
    if cards_per_player not in [1, 2]:
        await interaction.response.send_message("Number of cards per player must be 1 or 2!")
        return
    
    # Get voice channel members
    if not interaction.guild or not interaction.user.voice:
        await interaction.response.send_message("You must be in a voice channel to start the game!")
        return
        
    voice_channel = interaction.user.voice.channel
    members = voice_channel.members
    if len(members) < 2:
        await interaction.response.send_message("Need at least 2 players in the voice channel to start!")
        return
    
    # Get random themes
    themes = theme_manager.get_random_themes(3)
    if not themes:
        await interaction.response.send_message("No available themes! Please check the themes file.")
        return
    
    # Store themes for selection
    theme_states[channel_id] = themes
    
    # Create theme selection message with buttons
    theme_options = "\n".join(f"{i+1}. {theme}" for i, theme in enumerate(themes))
    embed = discord.Embed(
        title="🎲 New Ito Game!",
        description=f"Choose a theme:\n\n{theme_options}\n\nCards per player: {cards_per_player}",
        color=discord.Color.blue()
    )
    
    view = ThemeSelectView(themes, interaction, cards_per_player=cards_per_player)
    await interaction.response.send_message(embed=embed, view=view)

@app_commands.command(name="ito_submit", description="Select the next player in the sequence")
async def submit_arrangement(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    
    if channel_id not in active_games:
        await interaction.response.send_message("No active game in this channel!")
        return
        
    game = active_games[channel_id]
    
    if game.is_game_complete():
        await interaction.response.send_message("The game is already complete! Start a new game with /ito_start")
        return
    
    # Create player selection view
    view = PlayerSelectView(game, interaction)
    
    # Show current game status
    status_message = (
        f"Select the player for position {len(game.selected_players) + 1}\n\n"
        f"Lives remaining: ❤️ x {game.lives}\n\n"
        "Selected players so far:\n"
    )
    
    if game.selected_players:
        for i, (user_id, _) in enumerate(game.current_arrangement):
            player = game.players[user_id]
            member = interaction.guild.get_member(user_id)
            status_message += f"{i+1}. {player.color} {member.display_name}\n"
    else:
        status_message += "None\n"
    
    await interaction.response.send_message(status_message, view=view)

@app_commands.command(name="ito_end", description="End the current Ito game")
async def end_ito(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    
    if channel_id not in active_games:
        await interaction.response.send_message("No active game in this channel!")
        return
        
    active_games.pop(channel_id)
    if channel_id in theme_states:
        theme_states.pop(channel_id)
    await interaction.response.send_message("Game ended! Start a new game with /ito_start") 