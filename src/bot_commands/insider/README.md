# Insider Bot

The Insider Bot is a Discord bot designed to facilitate the game of Insider. This bot helps manage the game, ensuring smooth gameplay and an enjoyable experience for all participants.

## Features

- **Automated Game Management**: The bot handles the setup, progression, and conclusion of the game.
- **Role Assignment**: Automatically assigns roles to players, including the Insider, Master, and Commoners.
- **Word Selection**: Randomly selects a word for the game from a predefined list.
- **Logging**: Keeps track of used words to avoid repetition in future games.

## Usage

- **Running the Bot**: Start the bot by executing the main script.

  ```bash
  python bot.py
  ```

### Commands

- **`/insider`**: Start a new game of Insider.

  - Options:
    - `without`: Exclude specific players from being selected as the Insider.
    - `hide_insider`: Choose whether to hide the Insider's identity.
    - `minutes`: Set the duration of the game in minutes.
    - `custom_word`: Use a custom word for the game.
    - `use_file_words`: Use words from a predefined file instead of generating new ones.

- **`/end-insider`**: End the current game.
  - Only the user who started the session can end it.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
