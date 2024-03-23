import datetime


import telebot

from telebot.handler_backends import State, StatesGroup
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

from dbAdmin import createdb, get_user_stat, save_question

class MyStates(StatesGroup):
    question = State()
    answer= State()



def get_welcome() -> str:
    current_time = datetime.datetime.now()
    if 0<= current_time.hour <6:
        return 'Доброй ночи!'
    if 6<= current_time.hour <12:
        return 'Доброе утро!'
    if 12<= current_time.hour <18:
        return 'Добрый день!'
    else:
        return 'Добрый вечер!'

@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = f'{get_welcome()} Я бот, который подготовил для тебя интересный опрос✏\n\n'\
           f'Список команд:\n'\
           f'/get_all - получить общую статистику пользователей\n'\
           f'/add_question- добавить заметку \n'\
           f'/delete_question - удалить заметку'

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['get_all'])
def get_all(message: telebot.types.Message):
    bot.send_message(message.chat.id,get_user_stat())

@bot.message_handler(commands=['add_question'])
def get_all(message: telebot.types.Message):
    bot.set_state(message.from_user.id, MyStates.question, message.chat.id)
    bot.send_message(message.chat.id, 'Напишите вопрос')


@bot.message_handler(state=MyStates.question)
def add_question(message):
    bot.send_message(message.chat.id, 'Отлично, теперь напишите варианты ответов')
    bot.set_state(message.from_user.id, MyStates.answer, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['question'] = message.text
        save_question(data['question'])



if __name__=='__main__':
    print ('Бот запущен')
    bot.infinity_polling()