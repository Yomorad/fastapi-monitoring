import asyncio
from config import bot, dp
from handlers import register_handlers

async def main():
    # Регистрация обработчиков
    register_handlers(dp)

    # Запуск бота с polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
