# Discord Game Bot

A Discord bot designed to facilitate multiple party games including Insider, Ito, Just One, and Herd Mentality. This bot helps manage games, ensuring smooth gameplay and an enjoyable experience for all participants.

## Available Games

### Insider Game

A social deduction game where players try to guess a secret word while identifying the Insider.

#### Commands

- **`/insider`**: Start a new game of Insider
  - Options:
    - `minutes`: Set the duration of the game in minutes
    - `custom_word`: Use a custom word for the game
    - `use_file_words`: Use words from a predefined file
- **`/end-insider`**: End the current Insider game

### Ito Game

A cooperative party game where players arrange their secret numbers in ascending order through verbal clues.

#### Commands

- **`/ito_start`**: Start a new game of Ito
  - Options:
    - `cards_per_player`: Number of cards each player gets (minimum 1)
- **`/ito_submit`**: Submit your guess for the next number in the sequence
- **`/ito_end`**: End the current Ito game

### Just One Game

A cooperative word-guessing game where players provide one-word clues to help a player guess a target word.

#### Commands

- **`/just1`**: Start a new game of Just One
- **`/ja`**: Submit a clue for the current word
- **`/jremove`**: Remove your submitted clue
- **`/jshow_clue`**: Show all submitted clues
- **`/jreview`**: Review and filter similar clues
- **`/jend`**: End the current Just One game
- **`/jwithout`**: Exclude specific players from the game
- **`/jremove_without`**: Remove players from the exclusion list
- **`/jshow_rules`**: Display the game rules

### Herd Mentality Game

A party game where players try to match the most common answer given by the group.

#### Commands

- **`/start_session`**: Start a new Herd Mentality game session
- **`/start_round`**: Start a new round with a question
- **`/submit_answer`**: Submit your answer for the current question
- **`/show_answers`**: Display all submitted answers
- **`/show_results`**: Show the round results and scores
- **`/add_points_view`**: Manually adjust points
- **`/assign_cow`**: Assign the pink cow penalty
- **`/end_session`**: End the current game session
- **`/show_rules`**: Display the game rules

## Features

- **Voice Channel Integration**: Games require players to be in a voice channel
- **Automated Game Management**: Handles setup, progression, and conclusion of games
- **Role & Card Assignment**: Automatically assigns roles and cards to players
- **Theme System**: Ito game includes various themes for different gameplay experiences
- **Lives System**: Ito game includes a lives mechanic with rewards for perfect rounds
- **Private Messaging**: Sends secret information to players via DM
- **Multi-Game Support**: Can handle multiple games in different channels
- **Word Management**: Tracks used words to avoid repetition in word-based games
- **Score Tracking**: Maintains scores for competitive games
- **Player Exclusion**: Ability to exclude specific players from certain games
- **Customizable Settings**: Various options to customize game experiences

## Setup

1. Ensure the bot has necessary permissions in your Discord server
2. Join a voice channel
3. Use the appropriate command to start your desired game
4. Follow the bot's instructions for gameplay

## Requirements

- Discord.py library
- Python 3.8 or higher
- Bot must have permissions to:
  - Send messages
  - Send private messages
  - View channels
  - Read message history
  - Add reactions
  - Manage messages
  - Use external emojis

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
