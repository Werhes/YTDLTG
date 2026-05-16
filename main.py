import sys
sys.stdout.reconfigure(encoding='utf-8')# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router

async def main():
    # Включаем логирование, чтобы видеть ошибки в терминале
    logging.basicConfig(level=logging.INFO)
    
    # Инициализируем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутер с нашими обработчиками
    dp.include_router(router)
    
    print("🚀 Бот успешно запущен!")
    
    # Пропускаем старые сообщения и запускаем опрос
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")