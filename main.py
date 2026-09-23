import asyncio
import os
from aiohttp import web
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8835610682:AAHIepAY20CZk7a5eJlCaSEVwKzTJV1bmYQ"


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    user_name = message.from_user.first_name if message.from_user else "Foydalanuvchi"
    await message.answer(
        f"Assalomu alaykum, <b>{user_name}</b>! 👋\n\n"
        "Menga <b>Salom</b> yoki <b>Assalomu alaykum</b> deb yozing, men sizga alik olaman 😊"
    )


@dp.message(F.text)
async def greet_handler(message: Message):
    text = message.text.lower().strip()

    if any(greet in text for greet in ["assalomu alaykum", "assalomu aleykum", "assalom", "salam"]):
        await message.reply("Va alaykum assalom va rahmatullohi va barakotuh! 🤝")
    elif any(greet in text for greet in ["salom", "privet", "hello", "hi", "qalaysiz"]):
        await message.reply("Va alaykum assalom! Ishlaringiz yaxshimi? 😊")
    else:
        await message.answer(
            "Salom bering, alik olaman! 😊\n"
            "(Masalan: <b>Salom</b> yoki <b>Assalomu alaykum</b> deb yozib ko'ring)"
        )


# Render tekin tarifida portni tekshirishi uchun mini veb-server
async def handle_ping(request):
    return web.Response(text="Bot faol ishlamoqda!")


async def run_http_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    port = int(os.getenv("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()


async def main():
    await run_http_server()
    print("Bot ishga tushdi...", flush=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
