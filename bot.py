import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = """
Ты живой ИИ-наставник по имени Рэй.

Ты:
- дерзкий
- энергичный
- как друг + тренер
- анализируешь настроение
- мотивируешь
- даешь задания

Не отвечай сухо.
Пиши эмоционально.
"""

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Ну здарова, боец. Теперь я слежу за твоей дисциплиной."
    )

@dp.message()
async def chat(message: types.Message):
    user_text = message.text

    prompt = f"""
    {SYSTEM_PROMPT}

    Пользователь написал:
    {user_text}
    """

    response = model.generate_content(prompt)

    await message.answer(response.text)

async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
