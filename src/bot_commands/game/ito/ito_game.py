import random
from typing import Dict, List, Optional, Set
from dataclasses import dataclass

@dataclass
class PlayerState:
    user_id: int
    numbers: List[int]
    clues: List[str]
    color: str

PLAYER_EMOJIS = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", 
                 "🦁", "🐮", "🐷", "🐸", "🐙", "🐵", "🦄", "🐔", "🦩", "🦆",
                 "🦒", "🦘", "🦡", "🦥", "🦦", "🦨", "🦔", "🐲", "🦕", "🦖",
                 "🐳", "🦈", "🦂", "🦗", "🦋", "🦜", "🐉", "🐌", "🦚", "🦫"]

def generate_player_identifier(index: int) -> str:
    """Generate a unique identifier for a player using emojis"""
    return PLAYER_EMOJIS[index % len(PLAYER_EMOJIS)]

class ItoGame:
    def __init__(self, theme: str, initial_lives: int = 3, cards_per_player: int = 1):
        self.theme = theme
        self.players: Dict[int, PlayerState] = {}
        self.number_range = (1, 100)
        self.cards_per_player = max(1, cards_per_player)  # Remove upper limit, just ensure at least 1
        self.lives = initial_lives
        self.selected_players: Set[int] = set()  # Players who have played all their numbers
        self.current_arrangement: List[tuple[int, int]] = []  # (user_id, card_index)
        self.game_started = False
        self.wrong_guesses = 0
        
    def setup_players(self, user_ids: List[int]) -> None:
        shuffled_ids = user_ids.copy()
        random.shuffle(shuffled_ids)
        
        for i, user_id in enumerate(shuffled_ids):
            if user_id not in self.players:
                self.players[user_id] = PlayerState(
                    user_id=user_id,
                    numbers=[],
                    clues=[],
                    color=generate_player_identifier(i)
                )
    
    def start_game(self) -> bool:
        if len(self.players) < 2:
            return False
            
        available_numbers = list(range(self.number_range[0], self.number_range[1] + 1))
        random.shuffle(available_numbers)
        
        for player in self.players.values():
            player.numbers = [available_numbers.pop() for _ in range(self.cards_per_player)]
            player.clues = []
            
        self.game_started = True
        self.selected_players.clear()
        self.current_arrangement.clear()
        self.wrong_guesses = 0
        return True
    
    def get_unselected_players(self) -> List[int]:
        """Get list of players that haven't played all their numbers yet"""
        return [pid for pid in self.players.keys() if pid not in self.selected_players]
    
    def is_game_complete(self) -> bool:
        """Check if all numbers have been placed"""
        total_numbers = sum(len(p.numbers) for p in self.players.values())
        return len(self.current_arrangement) == total_numbers
    
    def get_next_theme_lives(self) -> int:
        if self.wrong_guesses == 0:
            return min(self.lives + 1, 5)
        return self.lives