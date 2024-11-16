import colorama
from colorama import Fore, Style
from constant.config import members_names
from tabulate import tabulate
import os

players = []

current_session = {
    "guesser": None,
    "clues": {},
    "word": None
}

colorama.init(autoreset=True)

def log_game_state(state, clues, guesser, removed_clues=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Current State: {state}")
    print("=" * 17)
    
    table_data = []
    removed_clues = removed_clues or set()
    
    for member in players:
        if isinstance(member, dict) and 'name' in member:
            if member['name'] == guesser:
                continue
            submission_status = "Submitted" if member['name'] in clues else "Not Submitted"
            color = Fore.GREEN if submission_status == "Submitted" else Fore.RED
            removed_status = "Yes" if member['name'] in removed_clues else "No"
            table_data.append([member['name'], f"{color}{submission_status}{Style.RESET_ALL}", removed_status])
    
    print(tabulate(table_data, headers=["Player Name", "Submit", "Removed"], tablefmt="grid"))