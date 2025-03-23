import os
import requests
import logging
import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from DataBase.database import async_main
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')


async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN')) 
    dp = Dispatcher() 
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router) # передаем роутер в диспетчер
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot) 

    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
