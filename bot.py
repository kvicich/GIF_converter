import asyncio
from telebot.async_telebot import AsyncTeleBot
import logging

with open('TOKEN.txt') as file:
    TOKEN = file.read()

bot = AsyncTeleBot(TOKEN)

# Хэндл '/start' и '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Привет! Это бот для конвертации видео в гифки, написан на telebot.\nЧто-бы начать использовать бот отправьте видео для конвертации'
    await bot.reply_to(message, text)

asyncio.run(bot.polling())