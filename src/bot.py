import discord
from constant.config import guild_id,token,bot
import sys
import os
import random

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

from bot_commands.game.ito import (
    start_ito,
    submit_arrangement,
    end_ito
)

from bot_commands.game.fetch_words import fetch_words
from bot_commands.random import random_person
from bot_commands.oat import oat
from bot_commands.question import question

from handle_screen_share_start import handle_screen_share_start

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
      
      #for Ito
      bot.tree.add_command(start_ito, guild=discord.Object(id=guild_id))
      bot.tree.add_command(submit_arrangement, guild=discord.Object(id=guild_id))
      bot.tree.add_command(end_ito, guild=discord.Object(id=guild_id))
      
      # Add fetch words command
      bot.tree.add_command(fetch_words, guild=discord.Object(id=guild_id))
      
      bot.tree.add_command(restart_bot, guild=discord.Object(id=guild_id))
      
      bot.tree.add_command(random_person, guild=discord.Object(id=guild_id))
      
      await bot.tree.sync(guild=discord.Object(id=guild_id))
      print("Commands synced successfully.")

  except Exception as e:
      print(f"Error syncing commands: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
  if member.id == bot.user.id:
      return

  voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)

#   TRIGGER_MEMBER_ID = 846709460146585610
#   TARGET_MEMBER_IDS = {612569701368856581,317304806647791619,435084115214073866}
  TRIGGER_MEMBER_ID = 0
  TARGET_MEMBER_IDS = {0}
  
  EXCLUDED_CHANNELS = {
      1273862909717643364,
      1283271249124135024,
      1273863622753255465,
      1273861439240802391,
      1288047044853891146,
      1273884418259288126,
      1273863713103020106,
      1273888909117362226,
      1273867188746452992
  }
  
  if (member.id == TRIGGER_MEMBER_ID and 
      after.channel and 
      (not before.channel or before.channel != after.channel)):
      
      target_members = []
      for channel_member in after.channel.members:
          if channel_member.id in TARGET_MEMBER_IDS:
              target_members.append(channel_member)
      
      if target_members:
          available_channels = [channel for channel in member.guild.voice_channels 
                               if channel != after.channel and 
                               channel.id not in EXCLUDED_CHANNELS and
                               (not channel.user_limit or len(channel.members) < channel.user_limit)]
          
          if available_channels:
              empty_channels = [channel for channel in available_channels if len(channel.members) == 0]
              
              if empty_channels:
                  print(f"Moving to empty channel(s)")
              else:
                  print(f"No empty channels available, moving to available channel(s)")
              
              for target_member in target_members:
                  if empty_channels:
                      random_channel = random.choice(empty_channels)
                  else:
                      random_channel = random.choice(available_channels)
                  
                  try:
                      await target_member.move_to(random_channel)
                      print(f"Moved member {target_member.display_name} from {after.channel.name} to {random_channel.name}")
                  except discord.Forbidden:
                      print(f"Bot doesn't have permission to move {target_member.display_name}")
                  except discord.HTTPException as e:
                      print(f"Failed to move member {target_member.display_name}: {e}")
          else:
              print("No available voice channels to move the target members to")

  if not before.self_stream and after.self_stream:
      await handle_screen_share_start(voice_client, after.channel, member)


@bot.tree.command(name="restart", description="Restarts the bot")
@discord.app_commands.checks.has_permissions(administrator=True)
async def restart_bot(interaction: discord.Interaction):
    await interaction.response.send_message("Restarting bot...")
    print("Bot restart initiated")
    os.execv(sys.executable, ['python'] + sys.argv)

bot.run(token)