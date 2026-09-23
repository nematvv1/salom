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
        "Men siz bilan salomlashadigan va hol-ahvol so'rashadigan botman.\n"
        "Menga bemalol: <b>Salom</b>, <b>Qalaysiz?</b> yoki <b>Ishlar qalay?</b> deb yozishingiz mumkin 😊"
    )


@dp.message(F.text)
async def chat_handler(message: Message):
    text = message.text.lower().strip()

    is_greeting = any(g in text for g in ["assalomu alaykum", "assalomu aleykum", "assalom", "salam", "salom", "privet", "hello", "hi"])
    is_asking_wellbeing = any(q in text for q in ["qalay", "yaxshimi", "tuzukmi", "ahvol", "charchama", "tinchmi", "nima gap"])

    # 1. Salomlashish va hol-ahvol birga kelganda
    if is_greeting and is_asking_wellbeing:
        await message.reply(
            "Va alaykum assalom! Rahmat, Alhamdulillah, o'zim juda yaxshiman! 🌟\n"
            "O'zingiz qandaysiz? Ishlaringiz, o'qishlaringiz yaxshi ketyaptimi? 😊"
        )
    # 2. Faqat salomlashish
    elif is_greeting:
        if any(g in text for g in ["assalomu alaykum", "assalomu aleykum", "assalom", "salam"]):
            await message.reply(
                "Va alaykum assalom va rahmatullohi va barakotuh! 🤝\n"
                "Qandaysiz, ahvollaringiz yaxshimi? Sog'-omonmisiz? 😊"
            )
        else:
            await message.reply(
                "Va alaykum assalom! Salom! 👋\n"
                "Qandaysiz? Ishlaringiz yaxshimi? Nima gaplar? 😊"
            )
    # 3. Botning hol-ahvolini so'raganda
    elif is_asking_wellbeing:
        await message.reply(
            "Rahmat, Xudoga shukr, a'lo darajadaman! 🚀\n"
            "O'zingiz qandaysiz? Charchamay yuribsizmi? Sizda nima yangiliklar? 😊"
        )
    # 4. "Nima qilyapsan" deb so'raganda
    elif any(act in text for act in ["nima qilyaps", "nima qivo", "nima ish qilyaps"]):
        await message.reply(
            "Siz bilan suhbatlashib, xabarlaringizga javob berib o'tiribman! 😊\n"
            "O'zingiz nimalar bilan bandsiz?"
        )
    # 5. Foydalanuvchi yaxshiligini aytganda
    elif any(pos in text for pos in ["yaxshi", "zo'r", "zor", "alhamdulillah", "shukur", "shukr", "tinch", "yaxshiman", "zo'rman", "joyida"]):
        await message.reply(
            "MashaAlloh, doimo yaxshi bo'ling! 🤲\n"
            "Kayfiyatingiz doim a'lo bo'lsin! Bugun nima rejalaringiz bor? ✨"
        )
    # 6. Foydalanuvchi charchaganini yoki ahvoli yomonligini aytganda
    elif any(neg in text for neg in ["yomon", "charchadim", "mazam yo'q", "kasal", "zerikdim", "kayfiyatim yo'q"]):
        await message.reply(
            "Iye, siqilmang! Har bir qiyinchilik ortida yaxshilik bor. 🌿\n"
            "Yaxshilab dam oling, o'zingizni ehtiyot qiling, tez orada hammasi zo'r bo'ladi! 😊"
        )
    # 7. Minnatdorchilik bildirganda
    elif any(thx in text for thx in ["rahmat", "tashakkur", "spasibo", "baraka top"]):
        await message.reply("Arzimaydi! Doimo xizmatingizdaman! 😊🤝")
    # 8. Boshqa har qanday xabarlar
    else:
        await message.answer(
            "Men bilan bemalol suhbatlashishingiz mumkin! 😊\n\n"
            "Masalan:\n"
            "• <b>Salom</b>\n"
            "• <b>Qalaysiz?</b>\n"
            "• <b>Ishlar qalay?</b>\n"
            "• <b>Nima qilyapsiz?</b> deb yozib ko'ring."
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
