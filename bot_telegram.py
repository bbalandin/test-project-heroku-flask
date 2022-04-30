from telegram.ext import Updater, MessageHandler, Filters
from random import choice
import sqlite3 as sql
import cryptocode

TOKEN = '5170550841:AAEPhHnLGtl03_QU7plUI3f6HfVkesshEGU'
sender = ''


def hashing(parameter):
    with open('keys.txt', 'r', encoding='utf-8') as file:
        key = file.read()
        str_encoded = cryptocode.encrypt(parameter, key)
    return str_encoded


def rehashing(parameter):
    with open('keys.txt', 'r', encoding='utf-8') as file:
        key = file.read()
        str_decoded = cryptocode.decrypt(parameter, key)
    return str_decoded


def db_get(_select, _from, _where=True, _param=0):
    db = sql.connect("db/AF.db")
    res = list(db.execute(f"SELECT {_select} FROM {_from} WHERE {_where}").fetchall())
    res2 = []
    for i in res:
        tmp = [i[j] for j in range(len(i))] if len(i) > 1 else i[0]
        res2.append(tmp)
    print(f'selected {_select} from {_from} where {_where}')
    print(f'db_get res: {res2}')
    return res2


def get_am():
    #f'рост: {res[0]}\nвес: {res[1]}\nталия: {res[2]}\nобхват бедер: {res[3]}\nобхват груди: {res[4]}'
    print(f'get_am({sender})')
    empty = 'Пустая антропометрия!'
    try:
        res = db_get("date_, height, weight, waist, hip_girth, bust",
                     "anthropometry",
                     f"user_id == (SELECT id FROM users WHERE id_telegram == '{sender}')")[0]
    except IndexError:
        return empty
    return f'Антропометрия за {res[0]}:\n' \
           f'Рост: {rehashing(res[1])}\n' \
           f'Вес: {rehashing(res[2])}\n' \
           f'Талия: {rehashing(res[3])}\n' \
           f'Обхват бедер: {rehashing(res[4])}\n' \
           f'Обхват груди: {rehashing(res[5])}'


answers = {
    '/help': [lambda:'Помощь по работе с ботом:\n/am - ваша антропометрия'],
    '/start': [lambda:f'Приветствую вас!\nЯ буду помогать вам тренероваться\n/help для подробностей'],
    '/am': [get_am],
    '/confirm': [lambda:'функция не работает'],
    '/reset': [lambda:'функция не работает']
}


def for_text(update, context):
    global sender
    sender = update.message["chat"]["username"]
    text = update.message.text.lower()
    answer = 'Произошла ошибка!'
    print('-' * 20)
    if sender in db_get("id_telegram", "users"):
        print(f'user {sender} was found in db')
        print(f'text: {text}')
        if text in answers.keys():
            print('building answer...')
            # собираем ответ, если нами учтен вопрос
            answer = str(answers[text][0]())
        if answer:
            print('sending answer...')
            # отсылаем ответ, если он собран и юзер пользуется telegram
            update.message.reply_text(answer)
            print(f'answer: {answer}')
            print('-' * 20)
    else:
        if not sender:
            update.message.reply_text("Укажите свое имя пользователя в настройках Telegram\n\n"
                                      "Для регистрации на сайте: link")
        else:
            update.message.reply_text("Что-то пошло не так!\n"
                                      "Вы указали верное имя пользователя Telegram?\n\n"
                                      f"Ваше имя пользователя: {sender}\n\n"
                                      "А если вы еще не зарегистрировались, самое время это сделать: link")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, for_text)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()