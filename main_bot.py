import telebot
from telebot import types
import csv
import pickle
import re
import schedule
import time
import threading
import datetime

from SQLighter import SQLighter
from config import token, sayhi, family_chat_id, admin_chat_id, poll_min_number
from weather_api import get_weather


# This is a main tree of received message.

def message_filter(message):

    if message.text in ['меню', 'Меню', '@renatakamilabot', 'Старт', 'старт', 'Начать', 'начать', 'Привет', 'привет', 'Назад']:
        # bot.send_message(message.chat.id,message.chat.id)
        # bot.send_message(message.chat.id, message.json['from']['first_name'])
        main_menue(message)

    #  WEATHER SECTION
    elif message.text in ['Погода',"погода"]: send_weather(message.chat.id)

    #  FOODSTUFF LIST SECTION
    elif message.text in ['Список Продуктов', 'Посмотреть список продуктов', 'Добавить продукты','Очистить']:
        if message.text == 'Список Продуктов': shopping_menue(message)
        elif message.text == 'Посмотреть список продуктов': show_shopping_list(message)
        elif message.text == 'Добавить продукты': add_to_shop_list(message)
        elif message.text == 'Очистить': delete_shoplist(message.chat.id)

    # CLEANING IN A HOUSE POLL AND STATISTICS SECTION
    elif message.text in ['Уборка',"уборка",'Заявить об уборке','Посмотреть баллы','Туалет','Кухня','Ванная','Коридор','Посуда']:
        if message.text in ['Уборка',"уборка"]: cleaning_menu(message)
        elif message.text == 'Заявить об уборке': cleaning_done_menu(message)
        elif message.text == 'Посмотреть баллы': get_scores(message)
        elif message.text in ['Туалет','Кухня','Ванная','Коридор','Посуда']: cleaning_committed(message)

    # WORD CENSORSHIP SECTION
    elif censorship(message.text): bot.delete_message(message.chat.id, message.id)


# This gives a user a main menu section buttons
def main_menue(message):
    if not message.chat.type == 'supergroup':
        menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        btn_weather = types.KeyboardButton(text='Погода')
        btn_store_list = types.KeyboardButton(text='Список Продуктов')
        btn_cleaning = types.KeyboardButton(text='Уборка')

        menu.add(btn_store_list, btn_cleaning, btn_weather)
        bot.send_message(message.chat.id, 'Вот список моих функций на сегодня. Пользуйся :) ', reply_markup=menu)

    else:
        menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        btn_weather = types.KeyboardButton(text='Погода')

        menu.add(btn_weather)
        bot.send_message(message.chat.id, 'Вот список моих функций на сегодня. Пользуйся :)', reply_markup=menu)


# These funcs gives a user a FOODSTUFF section buttons
def shopping_menue(message):
    bot.delete_message(message.chat.id, message.id)
    btn_back = types.KeyboardButton(text='Назад')
    btn_show_shopping_list = types.KeyboardButton(text='Посмотреть список продуктов')
    btn_add_to_shopping_list = types.KeyboardButton(text='Добавить продукты')

    shopping_menue = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    shopping_menue.add(btn_back, btn_show_shopping_list, btn_add_to_shopping_list)
    bot.send_message(message.chat.id, 'Ты можешь посмотреть или добавить в список продуктов ', reply_markup=shopping_menue)



def show_shopping_list(message):
    bot.delete_message(message.chat.id,message.id)
    bot.send_message(message.chat.id, '<b>Текущий список покупок:</b>', parse_mode='HTML')
    bot.send_message(message.chat.id, ', '.join(get_shoplist()))


def add_to_shop_list(message):
    sent = bot.send_message(message.chat.id, 'В следующем предложении ты можешь написать список продуктов <b>через пробел</b> или написать какой-то из них из списка и удалить его', parse_mode='HTML')
    bot.register_next_step_handler(sent, write_to_shoplist_from_message)


def get_shoplist():
    with open('shoplistfile.bin', 'rb') as file:
        temp_list = pickle.load(file)
        return temp_list

def delete_shoplist(chat_id):
    if chat_id == admin_chat_id:
        print('p')
        starting_list = ['Кефир']
        with open('shoplistfile.bin', 'wb') as file:
            pickle.dump(starting_list, file)

def write_to_shoplist_from_message(message):
    text = message.text
    text = text.lower()
    text = text.split(' ')
    for i in range(len(text)): text[i] = text[i][0].upper() + text[i][1:]

    temp_list = get_shoplist() + text
    temp_list = set(temp_list)
    temp_list = list(temp_list)

    with open('shoplistfile.bin', 'wb') as file:
        pickle.dump(temp_list, file)

# Weather and censorship section
def send_weather(chatid):
    weather , path = get_weather()
    bot.send_message(chatid, weather)
    with open(path, 'rb') as weather_icon:
        bot.send_photo(chatid, weather_icon)

def censorship(text):
    return text in ['плохой','какашка','шындырск']

# This gives a user a CLEANING menu section buttons
def cleaning_menu(message):
    menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_scores = types.KeyboardButton(text='Посмотреть баллы')
    btn_declare = types.KeyboardButton(text='Заявить об уборке')
    btn_back = types.KeyboardButton(text='Назад')

    menu.add(btn_declare, btn_scores, btn_back)
    sent = bot.send_message(message.chat.id, 'Выбери нужный пункт.', reply_markup=menu)

def cleaning_done_menu(message):
    menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_toilet = types.KeyboardButton(text='Туалет')
    btn_kitchen = types.KeyboardButton(text='Кухня')
    btn_bathroom = types.KeyboardButton(text='Ванная')
    btn_way = types.KeyboardButton(text='Коридор')
    btn_dishes = types.KeyboardButton(text='Посуда')
    btn_back = types.KeyboardButton(text='Назад')

    menu.add(btn_toilet,btn_kitchen,btn_bathroom,btn_way,btn_dishes,btn_back)
    sent = bot.send_message(message.chat.id, 'Что ты уже убрал?', reply_markup=menu)
    # bot.delete_message(sent.chat.id, sent.id)


# This Big Subsection works with polls:  create it, tracks votes, checks for finish conditions.
# If someone succsessfully cleans an area - his score updates. Currently thinking of moving it to an external class module.
def cleaning_committed(message):
    global poll_info_status

    if message.text == 'Кухня': points, half_point = 150 ,50
    else: points, half_point = 100, 50

    if not poll_info_status:

        name = message.json['from']['first_name']
        sender_id =  str(message.from_user.id)
        bot.send_poll(int(family_chat_id), f'Убрал ли {name} комнату {message.text}?',
                                  [ f'Да (+{points}б)', 'Нет(0б.)', f'50/50 (+{half_point}б.)' ], is_anonymous=False, type='regular',
                                  disable_notification=True)
        poll_info_status = True

        global poll_info_name, poll_info_place, poll_info_points,poll_info_half_points
        poll_info_name = sender_id
        poll_info_place = message.text
        poll_info_half_points = half_point


    else:
        bot.send_message(message.chat.id,'Одно голосование сейчас на проверке.Подождите, пожалуйста, а то я запутаюсь :)')



def poll_status_checker():

    global poll_info_status
    global opt_yes, opt_no, opt_mid
    global poll_info_name, poll_info_place, poll_info_points, poll_info_half_points

    if int(opt_yes) >= poll_min_number :

        bot.send_message(family_chat_id, 'Последнее голосование завершено, большинство согласно 😁')
        poll_info_status = False
        update_score(poll_info_name, poll_info_points, poll_info_place)

        opt_yes, opt_no, opt_mid = 0, 0, 0



    elif int(opt_no) >= poll_min_number - 1  :

        bot.send_message(family_chat_id,'Последнее голосование завершено, большинство не согласно 🤓')
        poll_info_status = False

        opt_yes, opt_no, opt_mid = 0, 0, 0


    elif int(opt_no) >= poll_min_number - 2 and opt_yes+opt_no+opt_mid >= poll_min_number:
        # Last poll is finished

        poll_info_status = False
        #  False = pole is finished so you can start a new one. True - is in progress, wait for smth
        bot.send_message(family_chat_id, 'Последнее голосование завершено, Не все согласны. Половоина баллов за уборку зачислено 🥴 ')
        update_score(poll_info_name, poll_info_half_points, poll_info_place)

        opt_yes, opt_no, opt_mid = 0, 0, 0

    else: pass


#  Keep tracking of a new votes in a telegram poll. Using poll_handler below
def process_new_poll_answer(poll):
    global opt_yes, opt_no, opt_mid

    answer = poll.option_ids[0]

    if answer == 0 : opt_yes += 1
    elif answer == 1 : opt_no += 1
    elif answer == 2: opt_mid +=1


# Return a current scores.
def get_scores(message):
    db = SQLighter('scores.db') # This is a class for working with database.

    res = db.get_all_scores()
    for j in range(len(res)): bot.send_message(message.chat.id, res[j])

    db.close()

def update_score(id,points,place):
    db = SQLighter('scores.db')
    db.up_score(id, points, place)
    db.close()


#  This section of 2 funcs should work with threadings and send a morning message at a special time in a morning.
def good_morning():
    bot.send_message(family_chat_id,'Доброе утро! Cегодня очередной прекрасный день')
    send_weather(family_chat_id)


def morning_checker():
    global poll_info_status
    schedule.every().day.at("05:40").do(good_morning)
    while True:
        if poll_info_status: poll_status_checker()
        time.sleep(1)

# Delete your /start message and send a welcome message
@bot.message_handler(commands=['start'])
def hello(message):
    # sayhi - starting message from a config.py
    bot.send_message(message.chat.id, sayhi)
    bot.delete_message(message.chat.id, message.id)

#  Process every message to a special sorting message tree
@bot.message_handler(content_types=['text'])
def main(message):
    message_filter(message)

@bot.poll_answer_handler(process_new_poll_answer)
def poll_answer_handler(_):
    pass

if __name__ == '__main__':

    global poll_info_status
    global opt_yes, opt_no
    opt_yes, opt_no, opt_mid= 0, 0, 0
    poll_info_status = False

    # Initializing a bot
    bot = telebot.TeleBot(token)

    # An infinite loop: if bot loses a connection, it restarts.
    while True:
        try:

            print('Включение', str(datetime.datetime.now().time())[:8])

            thread1 = threading.Thread(target=morning_checker)
            thread1.start()

            bot.polling(none_stop=True)
        except Exception as exc:
            print('Выключение', exc, str(datetime.datetime.now().time())[:8])
            time.sleep(15)