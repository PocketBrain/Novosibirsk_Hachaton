import asyncio
from aiogram import Bot, Dispatcher, types
import logging
from aiogram.utils import executor
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import *
from models import *
from fastapi import FastAPI, Depends
from ModelQA import *


users_data = {}


def tel_bot():
    load_dotenv()

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        #print(message.from_user.username)
        await message.answer("Привет! Я бот, который может помочь ответить на все ваши вопросы 🤗"
                             "\n/anketa - пройдите анкету, чтобы помочь нам стать лучше")

    @dp.message_handler(commands=['anketa'])
    async def start_message(message: types.Message):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('мужской', callback_data='pol_m'))
        keyboard.add(types.InlineKeyboardButton('женский', callback_data='pol_w'))
        await message.answer("Выберите ваш пол:", reply_markup=keyboard)


    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def text_message(message: types.Message):
        await message.answer('1)Ответ быстрой SBERT модели:')
        await message.answer(question_response(sbert_embeddings, message.text))
        await message.answer('2)GPT генерирует Ваш ответ, подождите, пожалуйста:')
        await message.reply(generate_gpt_response(message.text, modelgpt, tokenizer))


    @dp.callback_query_handler(lambda c: True)
    async def callback_answer(callback_query: types.CallbackQuery):
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


        keyboard = types.InlineKeyboardMarkup()

        if callback_query.data == 'pol_m':
            keyboard.add(types.InlineKeyboardButton('18-30', callback_data='18-30'))
            keyboard.add(types.InlineKeyboardButton('30-45', callback_data='30-45'))
            keyboard.add(types.InlineKeyboardButton('45+', callback_data='45+'))
            await bot.send_message(callback_query.from_user.id, 'Выберите ваш возраст:', reply_markup=keyboard)
            users_data[callback_query.message.chat.id] = ['m']
        elif callback_query.data == 'pol_w':
            keyboard.add(types.InlineKeyboardButton('18-30', callback_data='18-30'))
            keyboard.add(types.InlineKeyboardButton('30-45', callback_data='30-45'))
            keyboard.add(types.InlineKeyboardButton('45+', callback_data='45+'))
            await bot.send_message(callback_query.from_user.id, "Выберите ваш возраст:", reply_markup=keyboard)
            users_data[callback_query.message.chat.id] = ['w']
        elif callback_query.data == '18-30':
            keyboard.add(types.InlineKeyboardButton('IT', callback_data='IT'))
            keyboard.add(types.InlineKeyboardButton('маркетинг', callback_data='маркетинг'))
            keyboard.add(types.InlineKeyboardButton('HR', callback_data='HR'))
            keyboard.add(types.InlineKeyboardButton('Финансы', callback_data='Финансы'))
            keyboard.add(types.InlineKeyboardButton('продажи', callback_data='продажи'))
            await bot.send_message(callback_query.from_user.id, "Выберите вашу специальность :", reply_markup=keyboard)
            users_data[callback_query.message.chat.id].append('18-30')
        elif callback_query.data == '30-45':
            keyboard.add(types.InlineKeyboardButton('IT', callback_data='IT'))
            keyboard.add(types.InlineKeyboardButton('маркетинг', callback_data='маркетинг'))
            keyboard.add(types.InlineKeyboardButton('HR', callback_data='HR'))
            keyboard.add(types.InlineKeyboardButton('Финансы', callback_data='Финансы'))
            keyboard.add(types.InlineKeyboardButton('продажи', callback_data='продажи'))
            await bot.send_message(callback_query.from_user.id, "Выберите вашу специальность :", reply_markup=keyboard)
            users_data[callback_query.message.chat.id].append('30-45')
        elif callback_query.data == '45+':
            keyboard.add(types.InlineKeyboardButton('IT', callback_data='IT'))
            keyboard.add(types.InlineKeyboardButton('маркетинг', callback_data='маркетинг'))
            keyboard.add(types.InlineKeyboardButton('HR', callback_data='HR'))
            keyboard.add(types.InlineKeyboardButton('Финансы', callback_data='Финансы'))
            keyboard.add(types.InlineKeyboardButton('продажи', callback_data='продажи'))
            await bot.send_message(callback_query.from_user.id, "Выберите вашу специальность :", reply_markup=keyboard)
            users_data[callback_query.message.chat.id].append('45+')
        elif callback_query.data == 'IT':
            users_data[callback_query.message.chat.id].append('IT')
            print(users_data)
            to_create = User(
                id=callback_query.message.chat.id,
                pol=users_data[callback_query.message.chat.id][0],
                age_text=users_data[callback_query.message.chat.id][1],
                prof=users_data[callback_query.message.chat.id][2]
            )
            db: Session = SessionLocal()

            db.add(to_create)
            db.commit()
        elif callback_query.data == 'маркетинг':
            users_data[callback_query.message.chat.id].append('маркетинг')
            to_create = User(
                id=callback_query.message.chat.id,
                pol=users_data[callback_query.message.chat.id][0],
                age_text=users_data[callback_query.message.chat.id][1],
                prof=users_data[callback_query.message.chat.id][2]
            )
            db: Session = SessionLocal()

            db.add(to_create)
            db.commit()
            print(users_data)
        elif callback_query.data == 'HR':
            users_data[callback_query.message.chat.id].append('HR')
            to_create = User(
                id=callback_query.message.chat.id,
                pol=users_data[callback_query.message.chat.id][0],
                age_text=users_data[callback_query.message.chat.id][1],
                prof=users_data[callback_query.message.chat.id][2]
            )
            db: Session = SessionLocal()

            db.add(to_create)
            db.commit()
            print(users_data)
        elif callback_query.data == 'Финансы':
            users_data[callback_query.message.chat.id].append('Финансы')
            to_create = User(
                id=callback_query.message.chat.id,
                pol=users_data[callback_query.message.chat.id][0],
                age_text=users_data[callback_query.message.chat.id][1],
                prof=users_data[callback_query.message.chat.id][2]
            )
            db: Session = SessionLocal()

            db.add(to_create)
            db.commit()
            print(users_data)
        elif callback_query.data == 'продажи':
            users_data[callback_query.message.chat.id].append('продажи')
            to_create = User(
                id=callback_query.message.chat.id,
                pol=users_data[callback_query.message.chat.id][0],
                age_text=users_data[callback_query.message.chat.id][1],
                prof=users_data[callback_query.message.chat.id][2]
            )
            db: Session = SessionLocal()

            db.add(to_create)
            db.commit()
            print(users_data)

    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    tel_bot()