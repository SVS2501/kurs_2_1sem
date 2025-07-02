from telebot import types
import telebot
import sqlite3
name = None
current_category = None
token = 'токен не стоит выкладывать на гитхаб'
bot=telebot.TeleBot(token)
password = "let me in"
@bot.message_handler(commands=['start'])
def greetings(message): # приветствие и создание меню

    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS anecdotes (id int auto_increment primary key, category varchar, jokename varchar , joke varchar)')
    conn.commit()
    cur.close()
    conn.close()
    # создание кнопок
    markup= types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("1- добавить шутку ➕")
    item2 = types.KeyboardButton("2- удалить шутку ❌" )
    item3 = types.KeyboardButton("3- вывести случайную шутку 🎲")
    item4 = types.KeyboardButton("4- просмотреть все шутки 👁")
    item5 = types.KeyboardButton("5- прослушать озвученные шутки 🗣")
    markup.add(item1,item2,item3,item4,item5) #сборка меню
    bot.send_message(message.chat.id, "Привет, я бот, который хранит и рассказывает шутки ",reply_markup=markup) #отправка сообщения с приветствием
@bot.message_handler(commands=['randomjoke'])#случайная шутка
def randomjoke(message):
    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM anecdotes ORDER BY RANDOM() LIMIT 1') #выбор одной случайной шутки из базы
    jokenames = cur.fetchall()
    info = ''
    for el in jokenames:
        info += f'Категория {el[1]}, заголовок: {el[2]}, шутка: {el[3]}\n' #получение категории, заголовка и текста случайно выбранной шутки
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, "случайная шутка:")
    bot.send_message(message.chat.id, info)#вывод случайной шутки

@bot.message_handler(commands=['help']) #вывод справки
def help(message):
    bot.send_message(message.chat.id,"для того чтобы перезапустить меню пропишите в чате команду /start")
    bot.send_message(message.chat.id,"через кнопки меню в чате вы можете добавлять или удалять шутки,"
                                     " но для доступа к этой функции вам нужно ввести пароль"
                                     "\n ещё вы можете без пароля просмотреть все уже имеющиеся в базе шутки с помощью"
                                     " команды /show_jokes или кнопки 4- просмотреть все шутки 👁,\n "
                                     "также вы можете прослушать уже озвученные, нажав на кнопку 5- прослушать озвученные шутки 🗣")
@bot.message_handler(commands=["show_jokes"])#вывод всего содержимого из базы
def show_jokes(message):
    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM anecdotes') #выбор всего содержимого
    jokes = cur.fetchall()

    info = ''
    category=''
    viewed_categories=[]#массив с уже обработанными категориям
    for el in jokes:
        category=el[1]
        if category not in viewed_categories:
            info=''
            cur.execute(f"SELECT * FROM anecdotes WHERE category='{category}';")
            jokes_category=cur.fetchall()
            for elem in jokes_category:
                info += f'заголовок: {elem[2]}\n шутка: {elem[3]}\n'
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(f'категория: {el[1]}', callback_data='category.anecdotes'))
            bot.send_message(message.chat.id, info, reply_markup=markup)
            viewed_categories.append(category)#добавление категории в массив с уже обработанными категориями

    cur.close()
    conn.close()

@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == "1- добавить шутку ➕":
            bot.send_message(message.chat.id,"введите пароль") #запрос пароля
            bot.register_next_step_handler(message,password_check_add_joke)
        elif message.text == "2- удалить шутку ❌":
            bot.send_message(message.chat.id, "введите пароль") #запрос пароля
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
            #создание кнопок
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("🗣анекдот про зайца и медведя🐻🐇")
            item2=types.KeyboardButton("🗣заколдовал колдун мужика")
            item4 = types.KeyboardButton("🗣анекдот про ушлого студента")
            item5 = types.KeyboardButton("🗣генерал-захотел-сапоги-из-крокодила")
            item6 = types.KeyboardButton("🗣что будете делать если вам миллион дадут?")
            back = types.KeyboardButton("назад 🔙")
            markup.add(item1,item2,item4,item5,item6,back)#сбока меню
            bot.send_message(message.chat.id, "список озвученных шуток:", reply_markup=markup)
        elif message.text == "🗣анекдот про зайца и медведя🐻🐇":
            voice = open("C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\pjoect\\test.ogg",
                         'rb')
            bot.send_voice(message.chat.id, voice)
            voice.close()
        elif message.text =="🗣заколдовал колдун мужика":
            voice = open("C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\pjoect\\koldun.ogg",
                         'rb')
            bot.send_voice(message.chat.id, voice)
            voice.close()
        elif message.text =="🗣анекдот про ушлого студента":
            voice = open("C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\pjoect\\анекдот про ушлого студента.ogg",
                         'rb')
            bot.send_voice(message.chat.id, voice)
            voice.close()
        elif message.text =="🗣генерал-захотел-сапоги-из-крокодила":
            voice = open("C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\pjoect\\генерал-захотел-сапоги-из-крокодила.ogg",
                         'rb')
            bot.send_voice(message.chat.id, voice)
            voice.close()
        elif message.text =="🗣что будете делать если вам миллион дадут?":
            voice = open("C:\\Users\\sukov\\OneDrive\\Desktop\\лабы и практические\\3сем\\курсач\\pjoect\\если-вам-миллион-дадут.ogg",
                         'rb')
            bot.send_voice(message.chat.id, voice)
            voice.close()
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
            bot.send_message(message.chat.id, info)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("назад 🔙")
            item1 = types.KeyboardButton("ещё одна случайная шутка ")
            markup.add(item1,back)

        elif message.text == "назад 🔙": #кнопка для возврата в главное меню
            #создание кнопок
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("1- добавить шутку ➕")
            item2 = types.KeyboardButton("2- удалить шутку ❌")
            item3 = types.KeyboardButton("3- вывести случайную шутку 🎲")
            item4 = types.KeyboardButton("4- просмотреть все шутки 👁")
            item5 = types.KeyboardButton("5- прослушать озвученные шутки 🗣")
            markup.add(item1, item2, item3, item4, item5) #сборка меню
            bot.send_message(message.chat.id, "назад 🔙",reply_markup=markup)

password_checker = False

def password_check_add_joke(message): #проверка пароля для доступа к изменению базы
    global password_checker
    pswrd = message.text.strip() #ввод пароля
    if pswrd == password:
        password_checker = True
        bot.send_message(message.chat.id, "пароль верный, добро пожаловать")
        bot.send_message(message.chat.id, "Введите категорию шутки")
        bot.register_next_step_handler(message, joke_category)
    else:
        bot.send_message(message.chat.id, "пароль неверный.")

def joke_category(message):#ввод категории шутки
    global current_category
    current_category = message.text.strip()
    bot.send_message(message.chat.id, "введите название шутки")
    bot.register_next_step_handler(message,joke_name)

def joke_name(message):#ввод заголовка шутки
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "отправьте шутку одним текстовым сообщением")
    bot.register_next_step_handler(message, joke_text)

def joke_text(message): #ввод текста шутки
    joke = message.text.strip()#ввод
    #вставка в базу данных
    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()
    sql='INSERT INTO anecdotes (category, jokename, joke) VALUES (%s, %s, %s)'
    cur.execute("INSERT INTO anecdotes VALUES(?,?,?,?)",(None,current_category,name,joke))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('список шуток', callback_data='anecdotes'))
    bot.send_message(message.chat.id, "ваша шутка успешно добавлена!",reply_markup=markup)

def password_check_delete_joke(message):  #проверка пароля для доступа к изменению базы
    global password_checker
    pswrd = message.text.strip() #ввод пароля
    if pswrd == password:
        password_checker = True
        bot.send_message(message.chat.id, "пароль верный, добро пожаловать")
        bot.send_message(message.chat.id, "Введите заголовок шутки, которую хотите удалить")
        bot.register_next_step_handler(message, delete_joke)
    else:
        bot.send_message(message.chat.id, "пароль неверный.")

def delete_joke(message):
    deleting_name = message.text.strip()#ввод заголовка шутки, которую нужно удалить

    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()
    #удаление
    cur.execute(f"DELETE FROM anecdotes WHERE jokename='{deleting_name}';")
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('список шуток', callback_data='anecdotes'))
    bot.send_message(message.chat.id, f"Шутка с заголовком '{deleting_name}' удалена", reply_markup=markup)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("назад 🔙")
    markup.add(back)


@bot.callback_query_handler(func= lambda call: call.data.startswith("anecdotes"))
def callback(call):#вывод всей базы с разбиением на категории по нажатию кнопки

    conn = sqlite3.connect('anecdotes.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM anecdotes')
    jokes = cur.fetchall()

    info = ''
    category=''
    viewed_categories=[]
    for el in jokes:
        category=el[1]
        if category not in viewed_categories:
            info=''
            cur.execute(f"SELECT * FROM anecdotes WHERE category='{category}';")
            jokes_category=cur.fetchall()
            for elem in jokes_category:
                info += f'заголовок: {elem[2]}\n шутка: {elem[3]}\n'
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(f'категория: {el[1]}', callback_data='category.anecdotes'))
            bot.send_message(call.message.chat.id, info, reply_markup=markup)
            viewed_categories.append(category)

    cur.close()
    conn.close()

if __name__=='__main__':
    bot.infinity_polling()
