import telebot
import sqlite3 as sq
import time

bot = telebot.TeleBot('5887432555:AAECgVxzikZXu6pk9avMH9lAYPPH1i2ccsU')
bot.set_my_commands([
    telebot.types.BotCommand("/start", "в самое начало"),
    telebot.types.BotCommand("/clear", "очистить полностью базу данных"),
    telebot.types.BotCommand("/clear_user", "очистить данные пользователя"),
    telebot.types.BotCommand("/add", "обавить данные"),
    telebot.types.BotCommand("/print_db", "вывести базу данных"),
    telebot.types.BotCommand("/print_user", "вывести данные пользователя"),
])

tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'привет, {0.first_name}!'.format(message.from_user))
    bot.send_message(message.chat.id, 'начал создание базы данных')
    try:
        with sq.connect('test.db') as con:
            cur = con.cursor()
            cur.execute(f'''
            CREATE TABLE IF NOT EXISTS users_target(
                user_id INTEGER,
                name TEXT,
                date TEXT NOT NULL,
                msg_text TEXT
            )
            ''')
        bot.send_message(message.chat.id, 'база данных создана')
    except Exception as e:
        bot.send_message(message.chat.id, 'ошибка создания базы данных: {0}'.format(e))
        print(e)


@bot.message_handler(commands=['clear'])
def clear(message: telebot.types.Message):
    try:
        with sq.connect('test.db') as con:
            cur = con.cursor()
            cur.execute(f'''
            DROP TABLE IF EXISTS users_target
            ''')
        bot.send_message(message.chat.id, 'база данных очищена')
    except Exception as e:
        bot.send_message(message.chat.id, 'ошибка очистки базы данных: {0}'.format(e))


@bot.message_handler(commands=['clear_user'])
def clear_user(message: telebot.types.Message):
    try:
        with sq.connect('test.db') as con:
            cur = con.cursor()
            cur.execute(f'''
                        DELETE FROM users_target WHERE user_id = {message.chat.id}
                        ''')
        bot.send_message(message.from_user.id, 'пользователь удален из базы данных')
    except Exception as e:
        bot.send_message(message.from_user.id, 'ошибка удаления пользователя: {0}'.format(e))


@bot.message_handler(commands=['add'])
def add(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'отправьте сообщение для добавления в базу данных')
    bot.register_next_step_handler(message, add_data)


def add_data(message: telebot.types.Message):
    try:
        with sq.connect('test.db') as con:
            cur = con.cursor()
            cur.execute(f'''
            INSERT INTO users_target(name, user_id, date, msg_text)
            VALUES('{message.from_user.first_name}','{message.chat.id}', '{tconv(message.date)}' ,'{message.text}')
            ''')
        bot.send_message(message.chat.id, 'данные добавлены')
    except Exception as e:
        bot.send_message(message.chat.id, 'ошибка добавления данных: {0}'.format(e))


@bot.message_handler(commands=['print_db'])
def print_db(message: telebot.types.Message):
    try:
        with sq.connect('test.db') as con:
            cur = con.cursor()
            cur.execute(f'''
            SELECT * FROM users_target
            ''')
        bot.send_message(message.chat.id, f'{cur.fetchall()}')
    except Exception as e:
        bot.send_message(message.chat.id, 'ошибка вывода базы данных: {0}'.format(e))


@bot.message_handler(commands=['print_user'])
def print_user(message: telebot.types.Message):
    try:
        with sq.connect('test.db') as con:
            cur = con.cursor()
            cur.execute(f'''
            SELECT * FROM users_target WHERE user_id = {message.chat.id}
            ''')
        bot.send_message(message.chat.id, f'{cur.fetchall()}')
    except Exception as e:
        bot.send_message(message.chat.id, 'ошибка вывода пользователя: {0}'.format(e))


bot.polling(non_stop=True)
