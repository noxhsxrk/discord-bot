# Discord Bot

This is a Discord bot built using Python and the `discord.py` library. The bot is designed to interact with users in a Discord server, providing various functionalities such as joining voice channels, responding to messages, generating images, and more.

## Features

- **Voice Channel Interaction**: The bot can join voice channels and play audio files.
- **Message Handling**: Responds to user messages with text or images.
- **Scheduled Tasks**: Executes tasks at specified times.
- **OpenAI Integration**: Uses OpenAI's API for generating responses and images.
- **Language Detection**: Detects the language of user messages to tailor responses.

## Setup

### Prerequisites

- Python 3.8 or higher
- `discord.py` library
- `aiohttp` library
- `python-dotenv` library
- `openai` library
- `langdetect` library

### Installation

1. **Clone the repository**:
   bash
   git clone <https://github.com/noxhsxrk/discord-bot>
   cd discord-bot

2. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   - Create a `.env` file in the root directory.
   - Add the following variables:

     ```
     TOKEN=your_discord_bot_token
     GUILD_ID=your_guild_id
     OPENAI_API_KEY=your_openai_api_key
     MEMBERS_NAMES=[{"id": "member_id", "name": "member_name"}, ...]
     ```

4. **Prepare fixed times**:

   - Create a `src/constant/fixed_times.json` file with the following structure:

     ```json
     [
     {"task_name": "Task 1", "time": "08:00:00 GMT+7", "channel": 123456789012345678},
     ...
     ]
     ```

## Usage

- **Running the Bot**: Start the bot by executing the main script.

  ```
  python bot.py
  ```

- **Commands**:

  - `!oat`: Summon the bot to your voice channel.

- **Interactions**:
  - The bot responds to mentions and specific keywords in messages.
  - Automatically joins voice channels and plays audio when certain events occur.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) for the Discord API wrapper.
- [OpenAI](https://openai.com/) for the AI models used in generating responses and images.
