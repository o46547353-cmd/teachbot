import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.core.config import settings
from bot.handlers.registration import router as registration_router

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(registration_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())