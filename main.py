import asyncio
import os
from aiohttp import web
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8950461121:AAEt554fPm-geS6Mq7uTKc1a-fL5biAoNp4"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("ishladi")


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
