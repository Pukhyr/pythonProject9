import datetime


import telebot
from telebot import custom_filters, types


from telebot.handler_backends import State, StatesGroup
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

from dbAdmin import createdb, get_user_stat, save_question, save_answer, get_question, delete_questions, get_random


class MyStates(StatesGroup):
    question = State()
    answer= State()
    delete= State()



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

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = f'{get_welcome()} Я бот, который подготовил для тебя интересный опрос✏\n\n' \
           f'Список команд:\n' \
           f'/get_all - получить общую статистику пользователей\n' \
           f'/add_question- добавить вопрос \n' \
           f'/delete_question - удалить вопрос'

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вопрос")
    markup.add(btn1)
    text = f'{get_welcome()} Я бот, который подготовил для тебя интересный опрос✏, жми на кнопку, чтобы получить вопрос'
    bot.send_message(message.chat.id, text, reply_markup=markup)
@bot.message_handler(content_types=['text'])
def get_random_question(message):
    if(message.text == "Вопрос"):
        bot.send_message(message.chat.id, get_random())
    else:
        pass
bot.polling(none_stop=True)

@bot.message_handler(commands=['get_all'])
def get_all(message: telebot.types.Message):
    bot.send_message(message.chat.id,get_user_stat())

@bot.message_handler(commands=['add_question'])
def get_all(message: telebot.types.Message):
    bot.set_state(message.from_user.id, MyStates.question, message.chat.id)
    bot.send_message(message.chat.id, 'Напишите вопрос')


@bot.message_handler(state=MyStates.question)
def add_question(message):
    bot.send_message(message.chat.id, "Отлично, теперь напишите варианты ответов на отдельных строчках и через ';' номер вопроса, к которому они относятся")
    bot.set_state(message.from_user.id, MyStates.answer, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['question'] = message.text
        save_question(data['question'])

@bot.message_handler(state=MyStates.answer)
def add_question(message):
    bot.send_message(message.chat.id, "Варианты ответа были успешно добавлены")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['answers'] = message.text.split('\n')
        for answer in data['answers']:
            stroka=answer.split(';')
            if len(stroka) == 1:
                bot.send_message(message.chat.id,'Не было ";" ')
            elif len(stroka) == 2:
                number = stroka[1]
                content = stroka[0]
                save_answer(answers=content, question_id=int(number))
            else:
                bot.send_message(message.chat.id, 'Слишком много ";"')
    bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(commands=['delete_question'])
def delete_question(message: telebot.types.Message):
    bot.set_state(message.from_user.id, MyStates.delete, message.chat.id)
    bot.send_message(message.chat.id,'Выберите номер вопроса для удаления')
    bot.send_message(message.chat.id, get_question())

@bot.message_handler(state=MyStates.delete)
def add_question(message):
    bot.send_message(message.chat.id, "Вопрос, варианты ответа и статистика пользователей, ответивших на вопрос с этим номером, были удалены")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['number'] =message.text
        delete_questions(int(data['number']))
    bot.delete_state(message.from_user.id, message.chat.id)



bot.add_custom_filter(custom_filters.StateFilter(bot))

if __name__=='__main__':
    print ('Бот запущен')
    bot.infinity_polling()