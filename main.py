import datetime
import random

import telebot
from telebot import custom_filters

from dbAdmin import createdb, get_user_stat, save_question, save_answer, get_question, delete_questions, get_random, \
    get_choices, save_votes, user_stat, get_own, get_own_ques, get_own_choice, answered

from telebot.handler_backends import State, StatesGroup
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


class MyStates(StatesGroup):
    question = State()
    answer = State()
    delete = State()
    stattv = State()


def get_welcome() -> str:
    current_time = datetime.datetime.now()
    if 0 <= current_time.hour < 6:
        return 'Доброй ночи!'
    if 6 <= current_time.hour < 12:
        return 'Доброе утро!'
    if 12 <= current_time.hour < 18:
        return 'Добрый день!'
    else:
        return 'Добрый вечер!'


ADMIN_IDS = [234567890]


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = f'{get_welcome()} Я бот, который подготовил для тебя интересный опрос✏\n\n' \
           f'Список команд:\n' \
           f'Для админов:\n' \
           f'/get_all - получить общую статистику пользователей\n' \
           f'/add_question- добавить вопрос \n' \
           f'/delete_question - удалить вопрос \n'\
           f'Для пользователей:\n' \
           f'/get_random_question - получить рандомный вопрос, чтобы ответить, пришлите номер варианта ответа \n'\
           f'/get_my_own_stat - получить личную статистику'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['get_all'])
def get_all(message: telebot.types.Message):
    if message.from_user.id in ADMIN_IDS:
        all1 = get_user_stat()
        t = ''
        for i in all1:
            idtg = i[1]
            idque = i[2]
            idch = i[3]
            sque = get_own_ques(idque)
            sch = get_own_choice(idch)
            t += f'Id пользователя: {idtg}, вопрос: "{sque[0]}", ответ: "{sch[0]}"\n'
        bot.send_message(message.chat.id, t)
    else:
        bot.send_message(message.chat.id, "Нет прав")


@bot.message_handler(commands=['add_question'])
def add_ques(message: telebot.types.Message):
    if message.from_user.id in ADMIN_IDS:
        bot.set_state(message.from_user.id, MyStates.question, message.chat.id)
        bot.send_message(message.chat.id, 'Напишите вопрос')
    else:
        bot.send_message(message.chat.id, "Нет прав")


@bot.message_handler(commands=['delete_question'])
def delete_question(message: telebot.types.Message):
    if message.from_user.id in ADMIN_IDS:
        bot.set_state(message.from_user.id, MyStates.delete, message.chat.id)
        bot.send_message(message.chat.id, 'Выберите номер вопроса для удаления')
        quess = get_question()
        s = ''
        for i in quess:
            num = i[0]
            q = i[1]
            s += f'Номер: {num}, вопрос: {q}\n'
            bot.send_message(message.chat.id, s)
    else:
        bot.send_message(message.chat.id, "Нет прав")


@bot.message_handler(commands=['get_random_question'])
def get_rando(message: telebot.types.Message):
    tid = message.from_user.id
    answer = answered(tid)
    a = list(map(lambda x: x[0], answer))
    allid1 = get_question()
    al = list(map(lambda t: t[0], allid1))
    an = set(a)
    qe = set(al)
    allowed = list(qe-an)
    queid = random.choice(allowed)
    questoin_rand = get_random(queid)
    choic = get_choices(queid)
    s = ''
    for q in choic:
        idc = q[0]
        techo = q[1]
        s += f'Номер варианта ответа: {idc}, ответ: {techo}\n'
    bot.send_message(message.chat.id, questoin_rand)
    bot.send_message(message.chat.id, s)
    bot.set_state(message.from_user.id, MyStates.stattv, message.chat.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data['question_id'] = queid


@bot.message_handler(commands=['get_my_own_stat'])
def own_stat(message):
    userid = message.chat.id
    own = get_own(int(userid))
    s = ''
    for i in own:
        que = i[0]
        cho = i[1]
        ques = get_own_ques(que)
        choc = get_own_choice(cho)
        s += f'Вопрос: {ques[0]}...............Ваш ответ: {choc[0]}\n'
    bot.send_message(message.chat.id, s)


@bot.message_handler(state=MyStates.question)
def add_question(message):
    bot.send_message(message.chat.id, "Отлично, теперь напишите варианты ответов на отдельных строчках")
    bot.set_state(message.from_user.id, MyStates.answer, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        idp = save_question(message.text)
        data['question_id'] = idp


@bot.message_handler(state=MyStates.answer)
def add_question(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        question_id = data['question_id']
    for answer in message.text.split('\n'):
        save_answer(answers=answer, question_id=question_id)
    bot.send_message(message.chat.id, "Варианты ответа были успешно добавлены")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.delete)
def add_question(message):
    bot.send_message(message.chat.id, "Вопрос, варианты ответа и статистика пользователей, ответивших на этот вопрос, были удалены")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['number'] = message.text
        delete_questions(int(data['number']))
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.stattv)
def add_all(message):
    save_votes(int(message.text))
    userid = message.chat.id
    with bot.retrieve_data(message.from_user.id) as data:
        question_id = data['question_id']
    user_stat(tgid=int(userid), question_id=int(question_id), choice_id=int(message.text))
    bot.send_message(message.chat.id, "Ваш голос был добавлен")
    bot.delete_state(message.from_user.id, message.chat.id)


bot.add_custom_filter(custom_filters.StateFilter(bot))

if __name__ == '__main__':
    print('Бот запущен')
    bot.infinity_polling()
