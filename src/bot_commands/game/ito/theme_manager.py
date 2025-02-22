import random
import os
from typing import List, Optional

class ThemeManager:
    def __init__(self):
        self.themes_file = os.path.join(os.path.dirname(__file__), 'themes.txt')
        self.used_themes_file = os.path.join(os.path.dirname(__file__), 'used_themes.txt')
        
    def _read_themes(self, file_path: str) -> List[str]:
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
            
    def _write_theme(self, theme: str) -> None:
        with open(self.used_themes_file, 'a') as f:
            f.write(f"{theme}\n")
            
    def get_random_themes(self, count: int = 3) -> List[str]:
        all_themes = self._read_themes(self.themes_file)
        used_themes = self._read_themes(self.used_themes_file)
        
        # Filter out used themes
        available_themes = [t for t in all_themes if t not in used_themes]
        
        # If we're running low on themes, reset the used themes
        if len(available_themes) < count:
            available_themes = all_themes
            # Clear used themes file
            open(self.used_themes_file, 'w').close()
            
        # Return random themes
        return random.sample(available_themes, min(count, len(available_themes)))
        
    def mark_theme_as_used(self, theme: str) -> None:
        self._write_theme(theme) 