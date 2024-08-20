import os
import aiohttp
import discord
import openai
import time

async def generate_and_send_image(message, prompt):
  async with message.channel.typing():
      max_retries = 3
      for attempt in range(max_retries):
          try:
              print(f"Generating image with prompt: {prompt}")
              response = openai.Image.create(
                  model="dall-e-3",
                  prompt=prompt,
                  size="1024x1024",
                  n=1
              )

              image_url = response['data'][0]['url']
              print(f"Image generated successfully. URL: {image_url}")

              timeout = aiohttp.ClientTimeout(total=60)
              async with aiohttp.ClientSession(timeout=timeout) as session:
                  async with session.get(image_url) as resp:
                      async with message.channel.typing():
                          if resp.status == 200:
                              print("Downloading image...")
                              image_data = await resp.read()
                              with open("temp_image.png", "wb") as f:
                                  f.write(image_data)

                              with open("temp_image.png", "rb") as f:
                                  await message.reply(file=discord.File(f, "generated_image.png"))
                              print("Image sent to Discord channel.")

                              os.remove("temp_image.png")
                          else:
                              print("Failed to download the image.")
                              await message.reply("Failed to download the image.")
              break

          except openai.error.APIError as e:
              print(f"OpenAI API error: {e}")
              if attempt < max_retries - 1:
                  wait_time = 2 ** attempt
                  print(f"Retrying in {wait_time} seconds...")
                  time.sleep(wait_time)
              else:
                  await message.reply("An error occurred while generating the image. Please try again later.")
          except Exception as e:
              print(f"An error occurred during image generation: {e}")
              error_message = str(e)[:2000]
              await message.reply(f"An error occurred: {error_message}")
              break

async def handle_image_request(bot, message, content_lower):
  prompt = content_lower.replace(f"<@{bot.user.id}>", "").strip()
  for keyword in ["สร้าง", "สร้างรูป", "ขอรูป","รูป"]:
      prompt = prompt.replace(keyword, "").strip()

  if prompt:
      await generate_and_send_image(message, prompt)
  else:
      await message.reply("โปรดระบุคำอธิบายสำหรับรูปภาพที่คุณต้องการสร้าง")