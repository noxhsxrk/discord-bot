import os
import requests
import warnings
from discord import app_commands
from constant.config import load_dotenv
import discord

load_dotenv()
bearer_token = os.getenv('WORDS_API_TOKEN')

@app_commands.command(name="fw", description="Fetch words from API and update words.txt")
async def fetch_words(interaction: discord.Interaction):
    try:
        if not bearer_token:
            await interaction.response.send_message("Error: WORDS_API_TOKEN not found in .env file")
            return

        await interaction.response.send_message("Fetching words from API...")

        url = "https://www.noxhsxrk.com/api/words"
        headers = {
            "Authorization": f"Bearer {bearer_token}"
        }

        warnings.warn("SSL verification is disabled. Use this only if you trust the API endpoint.")
        
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        
        data = response.json()
        words = data.get("words", [])

        if not words:
            await interaction.edit_original_response(content="No words received from API.")
            return

        script_dir = os.path.dirname(os.path.abspath(__file__))
        words_file_path = os.path.join(script_dir, "words.txt")

        with open(words_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(words))

        await interaction.edit_original_response(
            content=f"Successfully updated words.txt with {len(words)} words!"
        )

    except requests.RequestException as e:
        await interaction.edit_original_response(
            content=f"Error fetching words from API: {str(e)}"
        )
    except Exception as e:
        await interaction.edit_original_response(
            content=f"An error occurred: {str(e)}"
        )
