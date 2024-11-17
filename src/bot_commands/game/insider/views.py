import discord

class WordSelectionView(discord.ui.View):
    def __init__(self, words, regenerate_callback):
        super().__init__()
        self.selected_word = None
        self.regenerate_callback = regenerate_callback

        for word in words:
            truncated_word = word[:80]
            button = discord.ui.Button(label=truncated_word, custom_id=truncated_word)
            button.callback = self.create_callback(truncated_word)
            self.add_item(button)

        regenerate_button = discord.ui.Button(
            label="สุ่มคำศัพท์ใหม่", 
            custom_id="regenerate", 
            style=discord.ButtonStyle.danger
        )
        regenerate_button.callback = self.regenerate_callback
        self.add_item(regenerate_button)

    def create_callback(self, word):
        async def callback(interaction: discord.Interaction):
            self.selected_word = word
            self.stop()
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(f"เลือกคำว่า '{word}' แล้ว", ephemeral=True)
                else:
                    await interaction.followup.send(f"เลือกคำว่า '{word}' แล้ว", ephemeral=True)
            except discord.errors.NotFound:
                print("ไม่สามารถส่งข้อความติดตามผล: ไม่พบ Webhook")
        return callback

class CountdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.stop_timer = False

    @discord.ui.button(label="หยุด", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop_timer = True
        self.stop()
        await interaction.response.send_message("หยุดจับเวลาและสิ้นสุดเซสชันแล้ว", ephemeral=True) 