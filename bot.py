import asyncio
from telebot.async_telebot import AsyncTeleBot
import logging
from moviepy.editor import VideoFileClip
import os

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

async def convert_video_to_gif(input_video_path, output_gif_path):
    logger.info("Начинается конвертация")
    # Загружаем видеофайл
    clip = VideoFileClip(input_video_path)

    # Ограничиваем длительность GIF (например, 10 секунд)
    if clip.duration > 10:
        clip = clip.subclip(0, 10)

    # Устанавливаем параметры GIF (опционально)
    clip = clip.set_fps(30)

    # Конвертируем видео в GIF
    clip.write_gif(output_gif_path, program='ffmpeg')

    # Закрываем клип
    clip.close()
    logger.info("Конвертация закончена")

@bot.message_handler(content_types=['video'])
async def handle_video(message):
    logger.info("Начинаем обработку...")
    # Скачиваем видео
    file_info = await bot.get_file(message.video.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    logger.info("Видео скачано")
    input_video_path = "input_video.mp4"
    output_gif_path = "output.gif"

    with open(input_video_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Конвертируем видео в GIF
    await convert_video_to_gif(input_video_path, output_gif_path)
    logger.info("Видео конвертировано")
    
    # Отправляем GIF обратно пользователю
    with open(output_gif_path, 'rb') as gif_file:
        await bot.send_document(message.chat.id, gif_file)
    logger.info("Гиф отправлена юзеру")
    
    # Удаляем временные файлы
    os.remove(input_video_path)
    os.remove(output_gif_path)
    logger.info("Обработка закончена.")

async def main():
    await bot.polling()

# Запуск основного цикла событий
if __name__ == '__main__':
    logger.info("Бот запускается...")
    asyncio.run(main())
    logger.info("Бот остановлен")