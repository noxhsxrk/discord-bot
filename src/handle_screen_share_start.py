from play_audio import play_audio
from members_names import member_name

async def handle_screen_share_start(voice_client, channel, member):
    if voice_client and voice_client.channel == channel:
        text_channel = voice_client.guild.get_channel(voice_client.channel.id)
        if text_channel:
            await play_audio(voice_client, 'sounds/can-you-see-the-screen.mp3')
            name = member_name.get(member.id, member.display_name)
            await text_channel.send(f"เห็นจอของ {name} กันมั้ยครับ")
        else:
            print("Text channel not found.")