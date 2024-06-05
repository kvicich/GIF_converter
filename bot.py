import asyncio
from telebot.async_telebot import AsyncTeleBot
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

with open('TOKEN.txt') as file:
    TOKEN = file.read()
    logger.info("Прочитан токен")

bot = AsyncTeleBot(TOKEN)
logger.info("Создан обьект бота")

# Хэндл '/start'
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    text = 'Привет! Это бот для конвертации видео в гифки, написан на telebot.\nЧто-бы начать использовать бот отправьте видео для конвертации'
    await bot.reply_to(message, text)
    logger.info("Использована команда /start")

async def main():
    await bot.polling()

# Запуск основного цикла событий
if __name__ == '__main__':
    logger.info("Бот запускается...")
    asyncio.run(main())
    logger.info("Бот остановлен")