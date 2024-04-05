import datetime


import telebot
from telebot import custom_filters


from telebot.handler_backends import State, StatesGroup
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

from dbAdmin import createdb, get_user_stat, save_question, save_answer, get_question, delete_questions, get_random, \
    get_choices, save_votes, user_stat


class MyStates(StatesGroup):
    question = State()
    answer= State()
    delete= State()
    stattv= State()



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

@bot.message_handler(commands=['start','help'])
def start_help(message: telebot.types.Message):
    text = f'{get_welcome()} Я бот, который подготовил для тебя интересный опрос✏\n\n' \
           f'Список команд:\n' \
           f'/get_all - получить общую статистику пользователей\n' \
           f'/add_question- добавить вопрос \n' \
           f'/delete_question - удалить вопрос \n'\
           f'/get_random_question - получить рандомный вопрос и варианты ответов, чтобы ответить пришлите номер варианта ответа \n'
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
    bot.send_message(message.chat.id, "Отлично, теперь напишите варианты ответов на отдельных строчках")
    bot.set_state(message.from_user.id, MyStates.answer, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        id=save_question(message.text)
        data['question_id']=id



@bot.message_handler(state=MyStates.answer)
def add_question(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        question_id = data['question_id']
    for answer in message.text.split('\n'):
        save_answer(answers=answer, question_id=question_id)
    bot.send_message(message.chat.id, "Варианты ответа были успешно добавлены")
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

@bot.message_handler(commands=['get_random_question'])
def get_rand(message: telebot.types.Message):
    record = get_random()
    question_id = record[0]
    ques=record[1]
    choic=get_choices(question_id)
    list=[]
    for q, w, e, r in choic:
        list.append((q, w))
    bot.send_message(message.chat.id, str(ques))
    bot.send_message(message.chat.id, str(list))
    bot.set_state(message.from_user.id, MyStates.stattv, message.chat.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data['question_id']=question_id



@bot.message_handler(state=MyStates.stattv)
def add_all(message):
    save_votes(int(message.text))
    userid=message.chat.id
    with bot.retrieve_data(message.from_user.id) as data:
        question_id=data['question_id']
    user_stat(tgid=int(userid),question_id=int(question_id) , choice_id=int(message.text))
    bot.send_message(message.chat.id, "Ваш голос был добавлен")
    bot.delete_state(message.from_user.id, message.chat.id)




bot.add_custom_filter(custom_filters.StateFilter(bot))

if __name__=='__main__':
    print ('Бот запущен')
    bot.infinity_polling()