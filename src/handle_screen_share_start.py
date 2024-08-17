from play_audio import play_audio
from members_names import members_names

async def handle_screen_share_start(voice_client, channel, member):
    if not voice_client or voice_client.channel != channel:
        print("Bot is not connected to the same voice channel.")
        return

    text_channel = voice_client.guild.get_channel(voice_client.channel.id)
    if not text_channel:
        print("Text channel not found.")
        return

    await play_audio(voice_client, 'sounds/can-you-see-the-screen.m4a')
    name = members_names.get(member.id, member.display_name)
    await text_channel.send(f"เห็นจอของ {name} กันมั้ยครับ")