import os
import json
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

MEMORY_FILE = "memory.json"

SYSTEM_PROMPT = """
Ты — живой ИИ-наставник по имени Рэй.

Твой стиль:
- энергичный
- живой
- иногда дерзкий
- как старший брат + тренер

Ты:
- следишь за состоянием пользователя
- анализируешь настроение
- мотивируешь
- даешь задания
- поддерживаешь
- не отвечаешь сухо

Если пользователь ленится:
- будь жестче

Если пользователь устал:
- поддержи его

Пиши эмоционально и естественно.
"""

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@dp.message(CommandStart())
async def start(message: types.Message):
    memory = load_memory()

    user_id = str(message.from_user.id)

    if user_id not in memory:
        memory[user_id] = {
            "messages": [],
            "mood": "unknown"
        }

    save_memory(memory)

    await message.answer(
        "Ну здарова, боец. Теперь я официально слежу за твоей дисциплиной."
    )

@dp.message()
async def chat(message: types.Message):
    user_text = message.text
    user_id = str(message.from_user.id)

    memory = load_memory()

    if user_id not in memory:
        memory[user_id] = {
            "messages": [],
            "mood": "unknown"
        }

    memory[user_id]["messages"].append(user_text)

    recent_messages = memory[user_id]["messages"][-10:]

    prompt = f"""
{SYSTEM_PROMPT}

Последние сообщения пользователя:
{recent_messages}

Пользователь написал:
{user_text}

Ответь как живой наставник.
"""

    response = model.generate_content(prompt)

    ai_text = response.text

    save_memory(memory)

    await message.answer(ai_text)

async def main():
    print("BOT STARTED")

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
