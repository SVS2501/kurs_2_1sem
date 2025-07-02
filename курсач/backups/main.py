from telebot import types
import telebot
import sqlite3
name = None
current_category = None
token = 'токен не стоит выкладывать на гитхаб'
bot=telebot.TeleBot(token)
password = "let me in"
@bot.message_handler(commands=['start'])
def greetings(message):

    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS anecdotes (id int auto_increment primary key, category varchar, jokename varchar , joke varchar)')
    conn.commit()
    cur.close()
    conn.close()

    #bot.send_message(message.chat.id, "Введите 1 если хотите добавить шутку, 2 если хотите удалить,3 если хотите случайную шутку, 4 если хотите просмотреть все шутки, 5 если хотите прослушать голосовое сообщение")
    markup= types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("1- добавить шутку ➕")
    item2 = types.KeyboardButton("2- удалить шутку ❌" )
    item3 = types.KeyboardButton("3- вывести случайную шутку 🎲")
    item4 = types.KeyboardButton("4- просмотреть все шутки 👁")
    item5 = types.KeyboardButton("5- прослушать озвученные шутки 🗣")
    item6 = types.KeyboardButton("6- как насчёт фокуса?✏")
    markup.add(item1,item2,item3,item4,item5,item6)
    bot.send_message(message.chat.id, "Привет, я бот, который хранит и рассказывает шутки ",reply_markup=markup)
    #bot.register_next_step_handler(message, choice)

@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == "1- добавить шутку ➕":
            bot.send_message(message.chat.id,"введите пароль")
            bot.register_next_step_handler(message,password_check_add_joke)
        elif message.text == "2- удалить шутку ❌":
            bot.send_message(message.chat.id, "введите пароль")
            bot.register_next_step_handler(message, password_check_delete_joke)
        elif message.text == "3- вывести случайную шутку 🎲":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("назад 🔙")
            item1 = types.KeyboardButton("ещё одна случайная шутка ")
            markup.add(item1,back)
            conn = sqlite3.connect('anecdotes.sql')
            cur = conn.cursor()

            cur.execute('SELECT * FROM anecdotes ORDER BY RANDOM() LIMIT 1')
            jokenames = cur.fetchall()
            info = ''
            for el in jokenames:
                info += f'Категория {el[1]}, название: {el[2]}, сама шутка: {el[3]}\n'
            cur.close()
            conn.close()
            bot.send_message(message.chat.id,"случайная шутка:",reply_markup=markup)
            bot.send_message(message.chat.id, info)

        elif message.text== "4- просмотреть все шутки 👁":
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('список шуток', callback_data='anecdotes'))
            bot.send_message(message.chat.id, "шутки", reply_markup=markup)

        elif message.text=="5- прослушать озвученные шутки 🗣":
            #audio = open(r"C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\pjoect\\test.mp3",'rb')
            #bot.send_audio(message.chat.id, audio)
            #audio.close()
            voice = open("C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\pjoect\\test.ogg",'rb')
            bot.send_voice(message.chat.id, voice)
            voice.close()
        elif message.text == "6- как насчёт фокуса?✏":
            video = open("C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\фокус.mp4",'rb')
            bot.send_video(message.chat.id,video)
            video.close()
        elif message.text=="ещё одна случайная шутка":

            conn = sqlite3.connect('anecdotes.sql')
            cur = conn.cursor()

            cur.execute('SELECT * FROM anecdotes ORDER BY RANDOM() LIMIT 1')
            jokenames = cur.fetchall()
            info = ''
            for el in jokenames:
                info += f'Категория {el[1]}, название: {el[2]}, сама шутка: {el[3]}\n'
            cur.close()
            conn.close()
            #bot.send_message(message.chat.id, "случайная шутка")
            bot.send_message(message.chat.id, info)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("назад 🔙")
            item1 = types.KeyboardButton("ещё одна случайная шутка ")
            markup.add(item1,back)
        elif message.text == "назад 🔙":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("1- добавить шутку ➕")
            item2 = types.KeyboardButton("2- удалить шутку ❌")
            item3 = types.KeyboardButton("3- вывести случайную шутку 🎲")
            item4 = types.KeyboardButton("4- просмотреть все шутки 👁")
            item5 = types.KeyboardButton("5- прослушать озвученные шутки 🗣")
            item6 = types.KeyboardButton("6- как насчёт фокуса?✏")
            markup.add(item1, item2, item3, item4, item5, item6)
            bot.send_message(message.chat.id, "назад 🔙",reply_markup=markup)


password_checker = False

def password_check_add_joke(message):
    global password_checker
    pswrd = message.text.strip()
    if pswrd == password:
        password_checker = True
        bot.send_message(message.chat.id, "пароль верный, добро пожаловать")
        bot.send_message(message.chat.id, "Введите категорию шутки (без кавычек)")
        bot.register_next_step_handler(message, joke_category)
    else:
        bot.send_message(message.chat.id, "пароль неверный.")

def password_check_delete_joke(message):
    global password_checker
    pswrd = message.text.strip()
    if pswrd == password:
        password_checker = True
        bot.send_message(message.chat.id, "пароль верный, добро пожаловать")
        bot.send_message(message.chat.id, "Введите название шутки, которую хотите удалить")
        bot.register_next_step_handler(message, delete_joke)
    else:
        bot.send_message(message.chat.id, "пароль неверный.")

def choice(message):
    variant = message.text.strip()
    if variant == "1":
        bot.send_message(message.chat.id,"введите пароль")
        bot.register_next_step_handler(message,password_check_add_joke)

    elif variant == "2":
        bot.send_message(message.chat.id, "введите пароль")
        bot.register_next_step_handler(message, password_check_delete_joke)

    elif variant =="3":

        conn = sqlite3.connect('anecdotes.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM anecdotes ORDER BY RANDOM() LIMIT 1')
        jokenames = cur.fetchall()
        info = ''
        for el in jokenames:
            info += f'Категория {el[1]}, название: {el[2]}, сама шутка: {el[3]}\n'
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, "случайная шутка")
        bot.send_message(message.chat.id, info)

    elif variant == "4":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('список шуток', callback_data='anecdotes'))
        bot.send_message(message.chat.id, "шутки", reply_markup=markup)
    elif variant =="5":
        audio = open(r"C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\pjoect\\test.mp3",'rb')
        bot.send_audio(message.chat.id,audio)
        audio.close()
        voice = open("C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\pjoect\\test.ogg",'rb')
        bot.send_voice(message.chat.id,voice)
        voice.close()

def joke_category(message):
    global current_category
    current_category = message.text.strip()
    bot.send_message(message.chat.id, "введите название шутки")
    bot.register_next_step_handler(message,joke_name)

def joke_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "отправьте шутку одним текстовым сообщением, в тексте шутки не должно быть кавычек")
    bot.register_next_step_handler(message, joke_text)

def joke_text(message):
    joke = message.text.strip()

    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO anecdotes (category, jokename, joke) VALUES ("%s", "%s","%s")'%(current_category,name,joke))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('список шуток', callback_data='anecdotes'))
    bot.send_message(message.chat.id, "ваша шутка успешно добавлена!",reply_markup=markup)

def delete_joke(message):
    deleting_name = message.text.strip()

    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()

    cur.execute(f"DELETE FROM anecdotes WHERE jokename='{deleting_name}';")
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('список шуток', callback_data='anecdotes'))
    bot.send_message(message.chat.id, f"Шутка с названием '{deleting_name}' удалена", reply_markup=markup)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("назад 🔙")
    markup.add(back)

@bot.callback_query_handler(func= lambda call: True)
def callback(call):

    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM anecdotes')
    jokes = cur.fetchall()

    info = ''
    for el in jokes:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(f'категория: {el[1]}', callback_data='anecdotes'))
        info += f'Категория: {el[1]}, название: {el[2]}, сама шутка: {el[3]}\n'
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id,info)

#@bot.message_handler(content_types=['text'])

@bot.message_handler(commands=['randomjoke'])
def randomjoke(message):
    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM anecdotes ORDER BY RANDOM() LIMIT 1')
    jokenames = cur.fetchall()
    info = ''
    for el in jokenames:
        info += f'Категория {el[1]}, название: {el[2]}, сама шутка: {el[3]}\n'
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, "случайная шутка:")
    bot.send_message(message.chat.id, info)

if __name__=='__main__':
    bot.infinity_polling()

