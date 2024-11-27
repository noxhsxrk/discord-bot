import discord
from constant.config import guild_id,token,bot
import sys
import os

from bot_commands.game.insider.insider import insider_command
from bot_commands.game.insider.end_insider import end_insider

from bot_commands.game.just_one.without import jwithout_command
from bot_commands.game.just_one.remove_without import jremove_without_command
from bot_commands.game.just_one.just_one import just1_command
from bot_commands.game.just_one.end_session import jend_command
from bot_commands.game.just_one.remove_clue import jremove_command
from bot_commands.game.just_one.review_clue import jreview_command
from bot_commands.game.just_one.show_clue import jshow_clue_command
from bot_commands.game.just_one.submit_clue import ja_command
from bot_commands.game.just_one.rule import jshow_rules

from bot_commands.game.herd_mentality.start_session import start_session
from bot_commands.game.herd_mentality.cow import assign_cow
from bot_commands.game.herd_mentality.rule import show_rules
from bot_commands.game.herd_mentality.add_points_view import add_points_view
from bot_commands.game.herd_mentality.end_session import end_session
from bot_commands.game.herd_mentality.show_answers import show_answers
from bot_commands.game.herd_mentality.show_results import show_results
from bot_commands.game.herd_mentality.start_round import start_round
from bot_commands.game.herd_mentality.submit_answer import submit_answer



from bot_commands.oat import oat
from bot_commands.question import question

from conversation_history import check_file_age, read_from_file, write_to_file
from get_openai_response import get_openai_response
from handle_screen_share_start import handle_screen_share_start
from handle_user_join_channel import handle_user_join_channel, pre_generate_messages
from image_generator import handle_image_request

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  try:
      bot.tree.clear_commands(guild=discord.Object(id=guild_id))
      bot.tree.add_command(oat, guild=discord.Object(id=guild_id))
      bot.tree.add_command(question, guild=discord.Object(id=guild_id))
      
      #for Herd Mentality
      bot.tree.add_command(start_session, guild=discord.Object(id=guild_id))
      bot.tree.add_command(start_round, guild=discord.Object(id=guild_id))
      bot.tree.add_command(submit_answer, guild=discord.Object(id=guild_id))
      bot.tree.add_command(add_points_view, guild=discord.Object(id=guild_id))
      bot.tree.add_command(show_answers, guild=discord.Object(id=guild_id))
      bot.tree.add_command(show_results, guild=discord.Object(id=guild_id))
      bot.tree.add_command(end_session, guild=discord.Object(id=guild_id))
      bot.tree.add_command(assign_cow, guild=discord.Object(id=guild_id))
      bot.tree.add_command(show_rules, guild=discord.Object(id=guild_id))
      
      #for Insider
      bot.tree.add_command(insider_command, guild=discord.Object(id=guild_id))
      bot.tree.add_command(end_insider, guild=discord.Object(id=guild_id))
      
      #for Just One
      bot.tree.add_command(just1_command, guild=discord.Object(id=guild_id))
      bot.tree.add_command(jremove_command, guild=discord.Object(id=guild_id))
      bot.tree.add_command(jend_command, guild=discord.Object(id=guild_id))
      bot.tree.add_command(jreview_command, guild=discord.Object(id=guild_id))
      bot.tree.add_command(ja_command, guild=discord.Object(id=guild_id))
      bot.tree.add_command(jshow_clue_command, guild=discord.Object(id=guild_id))
      bot.tree.add_command(jshow_rules, guild=discord.Object(id=guild_id))
      bot.tree.add_command(jwithout_command, guild=discord.Object(id=guild_id))
      bot.tree.add_command(jremove_without_command, guild=discord.Object(id=guild_id))  
      
      bot.tree.add_command(restart_bot, guild=discord.Object(id=guild_id))
      
      await bot.tree.sync(guild=discord.Object(id=guild_id))
      print("Commands synced successfully.")
      
    #   await pre_generate_messages()
    #   print("Pre-generated messages loaded successfully.")
  except Exception as e:
      print(f"Error syncing commands: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
  if member.id == bot.user.id:
      return

  voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)

  if not before.self_stream and after.self_stream:
      await handle_screen_share_start(voice_client, after.channel, member)

  if after.channel and after.channel != before.channel:
      await handle_user_join_channel(voice_client, after.channel, member)

@bot.event
async def on_message(message):
  if message.author.bot:
      return

  channel_id = message.channel.id

  check_file_age(channel_id)

  write_to_file(channel_id, "user", message.content)

  if bot.user.mentioned_in(message):
      content_lower = message.content.lower()
      if any(keyword in content_lower for keyword in ["สร้าง", "สร้างรูป", "ขอรูป", "รูป"]):
          await handle_image_request(bot, message, content_lower)
      else:
          async with message.channel.typing():
              conversation_history = read_from_file(channel_id)
              conversation_text = "\n".join(
                  f"{entry['role']}: {entry['content']}" for entry in conversation_history
              )

              response = await get_openai_response(conversation_text, 250, message.author.id)
              await message.reply(response)

              write_to_file(channel_id, "assistant", response)

@bot.tree.command(name="restart", description="Restarts the bot")
@discord.app_commands.checks.has_permissions(administrator=True)
async def restart_bot(interaction: discord.Interaction):
    await interaction.response.send_message("Restarting bot...")
    print("Bot restart initiated")
    os.execv(sys.executable, ['python'] + sys.argv)

bot.run(token)