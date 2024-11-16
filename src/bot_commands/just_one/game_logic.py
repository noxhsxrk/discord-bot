import colorama
from colorama import Fore, Style
from constant.config import active_lumi_members
from tabulate import tabulate
import os

current_session = {
    "active_player": None,
    "clues": {},
    "word": None
}

colorama.init(autoreset=True)

def log_game_state(state, clues, active_player, removed_clues=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Current State: {state}")
    print("=" * 17)
    
    table_data = []
    removed_clues = removed_clues or set()
    for member in active_lumi_members:
        if member['name'] == active_player:
            continue
        submission_status = "Submitted" if member['name'] in clues else "Not Submitted"
        color = Fore.GREEN if submission_status == "Submitted" else Fore.RED
        removed_status = "Yes" if member['name'] in removed_clues else "No"
        table_data.append([member['name'], f"{color}{submission_status}{Style.RESET_ALL}", removed_status])
    
    print(tabulate(table_data, headers=["Player Name", "Submit", "Removed"], tablefmt="grid"))