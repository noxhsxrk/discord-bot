import os
import time
from collections import Counter
from .constants import INSIDER_DIRECTORY, INSIDER_LOG_FILE

def get_session_file_path(user_id, insider_name, word, status="active"):
    return os.path.join(INSIDER_DIRECTORY, f"insider_session_{user_id}_{insider_name}_{word}_{status}.log")

def log_insider_selection(insider_name, word):
    log_file_path = os.path.join(INSIDER_DIRECTORY, INSIDER_LOG_FILE)
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{insider_name},{word},{int(time.time())}\n")

def get_insider_selection_counts():
    try:
        log_file_path = os.path.join(INSIDER_DIRECTORY, INSIDER_LOG_FILE)
        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()
            insider_names = [line.split(',')[0] for line in lines]
            return Counter(insider_names)
    except FileNotFoundError:
        return Counter()

def get_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def get_used_words(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(line.strip() for line in file.readlines())

def write_used_word(file_path, word):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{word}\n")