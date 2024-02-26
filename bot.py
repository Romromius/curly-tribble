from telebot.async_telebot import AsyncTeleBot
import asyncio
import sqlite3

with open('token', 'r') as f:
    BOT_TOKEN = f.read()
bot = AsyncTeleBot(BOT_TOKEN)

sessions = []

db = sqlite3.connect('db.sqlite')
cur = db.cursor()


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    for i in sessions:
        if i[0] == message.from_user.id:
            sessions.remove(i)
    await bot.send_message(message.from_user.id, "С помощью этого бота вы можете оставить свой отзыв\\\n\n"
                                                 "Для начала работы отправьте краткое описание темы вашего отзыва\\\n"
                                                 "_Постарайтесь как можно точнее описать суть вашего обращения_",
                           parse_mode='MarkdownV2')


@bot.message_handler(func=lambda msg: True)
async def echo_all(message):
    for session in sessions:
        if session[0] == message.from_user.id:
            await bot.send_message(message.from_user.id, 'Ваше обращение сохранено.')
            sessions.remove(session)
            cur.execute(f'INSERT INTO responses VALUES(NULL, {session[0]}, "{session[1]}", "{message.text}")')
            db.commit()
            print('Новое обращение от', message.from_user.username)
            return
    sessions.append([message.from_user.id, message.text])
    await bot.send_message(message.from_user.id, 'Теперь отправьте текст вашего обращения.')


asyncio.run(bot.polling())
