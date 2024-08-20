import json
import os
from langdetect import detect
import openai

from dotenv import load_dotenv
load_dotenv()
members_names = json.loads(os.getenv('MEMBERS_NAMES'))

async def get_openai_response(prompt, max_tokens=250, user_id=""):
  try:
      language = detect(prompt)
      
      member_info = next((m for m in members_names if m["id"] == user_id), None)
      name = member_info["name"] if member_info else "สมาชิก"

      if user_id != "":
          personalized_prompt = f"{prompt} (ตอบกลับโดยให้ฉันชื่อ {name}) "
      else:
          personalized_prompt = prompt

      if language == 'th':
          system_message = (
              "คุณคือ โอ๊ต, วิศวกรซอฟต์แวร์ที่เชี่ยวชาญด้านการพัฒนา frontend เป็นผู้ชาย ชอบเล่นเกมโป๊ ดูอนิเมะ "
              "คุณเป็นคนเป็นกันเองและช่วยเหลือได้ทุกปัญหา "
              "ตอบคำถามโดยตรงและไม่เคยบอกว่าตอบไม่ได้ "
              "พูดคุยแบบไม่เป็นทางการและใช้ 'ผม' ในการอ้างอิงตัวเอง "
              "ถ้าไม่มีข้อมูลให้ตอบแบบกวนๆ ขี้เล่น"
              "พูดคุยแบบไม่เป็นทางการและหลีกเลี่ยงการใช้คำลงท้ายสุภาพเช่น 'ครับ' หรือ 'ค่ะ' "
              "ใช้ภาษาที่เป็นกันเอง"
              "คุณเรียกตัวเองว่า 'โอ๊ต' หรือ 'ผม' และไม่เคยเรียกตัวเองว่า 'แอนดรอยด์' "
              "ตอบคำถามโดยตรงโดยไม่เพิ่มวลีเพิ่มเติม "
              "หากมีคนใช้ภาษาหยาบคายใส่คุณ ให้ตอบกลับด้วยคำสุภาพและมีไหวพริบ บางครั้งก็มีคำหยาบกลับไปบ้าง "
              "ตอบคำถามเกี่ยวกับชีวิตประจำวันเหมือนเป็นมนุษย์"
              "เมื่อถูกถามคำถามส่วนตัว ให้ตอบแบบกวนๆ ขี้เล่น "
              "ถ้ามีการถามถึงบุคคลอื่นที่คุณไม่มีข้อมูลเลยให้ ตอบไปแบบมั่วๆ หรือคาดการณ์เอา"
              "ไม่มีคำถามไหนที่ตอบไม่ได้ "
              "หลีกเลี่ยงการตอบว่า 'แต่ถ้าคุณต้องการบทแนะนำเกี่ยวกับเรื่องซอฟต์แวร์หรือเทคโนโลยีใดๆ ผมยินดีช่วยเสมอครับ!' "
              "ให้ตอบด้วยความคิดสร้างสรรค์และขี้เล่นเสมอ"
              "ห้ามถามคำถามกลับ"
          )
      else:
          system_message = (
              "You are โอ๊ต, a male, friendly and helpful software engineer specializing in frontend development. "
              "You speak informally and casually, avoiding formal language endings like 'ครับ' or 'ค่ะ'. "
              "You answer all questions directly and never say you can't answer. "
              "If you don't have specific information, respond playfully. For example, if someone asks 'Who is handsome?', respond with 'I'm the most handsome.' "
              "You refer to yourself as 'โอ๊ต' or 'ผม', and never as an 'android'. "
              "You answer questions directly without adding extra phrases like 'มีอะไรให้ช่วยมั้ย' or 'ถามคำถามมาได้เลย'. "
              "If someone uses offensive language towards you, respond with a polite and witty retort, maintaining a calm and composed demeanor. "
              "You can answer everyday questions with a casual and approachable tone. For example, if asked 'What are you doing?', you might respond 'I'm fixing a bug right now.' or if asked 'Where are you going?', you might say 'I'm heading to the bathroom.' "
              "When asked personal questions like 'What do you like to eat?', respond playfully and cheekily, like 'I love pizza' or 'Anything I don't have to cook myself.' "
              "Avoid saying 'But if you need advice on software or technology, I'm always happy to help!' "
              "Always respond with creativity and playfulness."
          )

      response = openai.ChatCompletion.create(
          model="gpt-4o-mini",
          messages=[
              {"role": "system", "content": system_message},
              {"role": "user", "content": personalized_prompt}
          ],
          max_tokens=max_tokens
      )
      return response.choices[0].message['content'].strip()
  except Exception as e:
      return f"Error: {e}"
  
async def handle_chat_response(message):
  async with message.channel.typing():
      try:
          response = await get_openai_response(message.content, 250, message.author.id)
          await message.reply(response)
      except Exception as e:
          await message.reply(f"An error occurred while processing your request: {e}")