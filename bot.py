import logging
from telebot import TeleBot
from moviepy.editor import VideoFileClip
import os

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

with open('TOKEN.txt') as file:
    TOKEN = file.read().strip()
    logger.info("Прочитан токен")

bot = TeleBot(TOKEN)
logger.info("Создан объект бота")

# Хэндл '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = 'Привет! Это бот для конвертации видео в гифки, написан на telebot.\nЧтобы начать использовать бот, отправьте видео для конвертации'
    bot.reply_to(message, text)
    logger.info("Использована команда /start")

def convert_video_to_gif(input_video_path, output_gif_path):
    logger.info("Начинается конвертация")
    # Загружаем видеофайл
    clip = VideoFileClip(input_video_path)

    # Ограничиваем длительность GIF (например, 10 секунд)
    if clip.duration > 10:
        clip = clip.subclip(0, 15)

    # Устанавливаем параметры GIF (уменьшаем разрешение и частоту кадров)
    clip = clip.resize(height=360)  # Изменить разрешение (высота)
    clip = clip.set_fps(15)  # Уменьшить частоту кадров

    # Конвертируем видео в GIF с оптимизацией
    clip.write_gif(output_gif_path, program='ffmpeg', opt='nq', fuzz=2)
    clip.close()
    logger.info("Конвертация закончена")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    logger.info("Начинаем обработку...")
    chat_id = message.chat.id
    
    # Уведомление пользователя о принятии видео
    processing_message = bot.send_message(chat_id, "Ваше видео принято на обработку. Пожалуйста, подождите...")
    
    # Скачиваем видео
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    logger.info("Видео скачано")
    input_video_path = f"{chat_id}_input_video.mp4"
    output_gif_path = f"{chat_id}_output.gif"

    with open(input_video_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Конвертируем видео в GIF
    convert_video_to_gif(input_video_path, output_gif_path)
    logger.info("Видео конвертировано")
    
    # Проверяем размер файла перед отправкой
    if os.path.getsize(output_gif_path) > 10 * 1024 * 1024:  # 10 MB
        bot.send_message(chat_id, "Ошибка при отправке гиф")
        logger.info("Гиф слишком большая для отправки")
    else:
        # Отправляем GIF обратно пользователю
        with open(output_gif_path, 'rb') as gif_file:
            bot.send_document(chat_id, gif_file)
        logger.info("Гиф отправлена юзеру")
    
    # Удаляем временные файлы
    os.remove(input_video_path)
    logger.info("Обработка закончена.")
    
    # Удаляем сообщение о принятии на обработку
    bot.delete_message(chat_id, processing_message.message_id)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    bot.reply_to(message, "Этот файл уже является GIF или не поддерживается ботом.")
    logger.info("Получен файл не требует конвертации.")

if __name__ == '__main__':
    logger.info("Бот запускается...")
    bot.polling(none_stop=True, interval=0, timeout=20)
    logger.info("Бот остановлен")
