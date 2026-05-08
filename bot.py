import os
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import google.generativeai as genai

# Загрузка .env

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini

genai.configure(api_key=GEMINI_API_KEY)

# Более стабильная модель

model = genai.GenerativeModel("gemini-1.5-flash")

# Telegram

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Файл памяти

MEMORY_FILE = "memory.json"

# Характер бота

SYSTEM_PROMPT = """
Ты — живой ИИ-наставник по имени Рэй.

Твой стиль:

* энергичный
* живой
* эмоциональный
* иногда дерзкий
* как старший брат + тренер + друг

Ты:

* следишь за состоянием пользователя
* мотивируешь
* анализируешь настроение
* поддерживаешь
* даешь задания
* иногда шутишь

Если пользователь ленится:

* будь жестче

Если пользователь устал:

* поддержи его

Не отвечай как ChatGPT.
Пиши как живой человек.
"""

# Загрузка памяти

def load_memory():
try:
with open(MEMORY_FILE, "r", encoding="utf-8") as f:
return json.load(f)
except:
return {}

# Сохранение памяти

def save_memory(data):
with open(MEMORY_FILE, "w", encoding="utf-8") as f:
json.dump(data, f, ensure_ascii=False, indent=2)

# Команда /start

@dp.message(CommandStart())
async def start(message: types.Message):

```
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
```

# Обычные сообщения

@dp.message()
async def chat(message: types.Message):

```
try:
    user_text = message.text
    user_id = str(message.from_user.id)

    memory = load_memory()

    if user_id not in memory:
        memory[user_id] = {
            "messages": [],
            "mood": "unknown"
        }

    # Сохраняем сообщение
    memory[user_id]["messages"].append(user_text)

    # Последние 10 сообщений
    recent_messages = memory[user_id]["messages"][-10:]

    # Промпт
    prompt = f"""
```

{SYSTEM_PROMPT}

Последние сообщения пользователя:
{recent_messages}

Пользователь написал:
{user_text}

Ответь как живой наставник.
"""

```
    # Ответ Gemini
    response = model.generate_content(prompt)

    ai_text = response.text

    # Сохраняем память
    save_memory(memory)

    # Отправляем ответ
    await message.answer(ai_text)

except Exception as e:
    print("ERROR:", e)

    await message.answer(
        "Бро, у меня мозг на секунду завис. Напиши еще раз."
    )
```

# Запуск

async def main():

```
print("BOT STARTED")

# Удаляем конфликтующие webhook/polling
await bot.delete_webhook(drop_pending_updates=True)

# Запуск бота
await dp.start_polling(bot)
```

# Старт программы

if **name** == "**main**":
asyncio.run(main())

