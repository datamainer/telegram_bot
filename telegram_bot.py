import random

import telebot
from bs4 import BeautifulSoup
import requests
from time import sleep

TOKEN = '1982714627:AAGxOtxmSnOcXcwYAtA0sDqt-TSBfCEmaUs'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '''
Поиск по Авито (Локация: Петрозаводск): 
/avito 

Поиск по YouTube: 
/youtube

Cоздание ссылок по никнейму юзера в инстаграм: 
/instagram

Сгенерировать пароль:
/create_pass

''')


###################################################################################
@bot.message_handler(commands=['avito'])
def avito(message):
    bot.send_message(message.chat.id, 'Поиск по Авито')
    sleep(1)
    msg = bot.send_message(message.chat.id, 'Что ищем ?')
    bot.register_next_step_handler(msg, avito_search)


def avito_search(message):
    url = 'https://www.avito.ru/petrozavodsk?q=' + message.text
    request = requests.get(url)
    bs = BeautifulSoup(request.text, 'html.parser')
    all_links = bs.find_all('a', class_="title-listRedesign-_rejR")
    print(all_links)

    pages = 0
    for link in all_links:
        links = 'https://www.avito.ru' + link['href']
        bot.send_message(message.chat.id, links)
        pages += 1
        print(links)
        if pages == 10:
            break


####################################################################################
@bot.message_handler(commands=['youtube'])
def youtube(message):
    bot.send_message(message.chat.id, 'Поиск по YouTube')
    sleep(1)
    msg = bot.send_message(message.chat.id, 'Что ищем ?')
    bot.register_next_step_handler(msg, youtube_search)


def youtube_search(message):
    url = 'https://www.youtube.com/results?search_query=' + message.text
    print(url)
    request = requests.get(url)
    bs = BeautifulSoup(request.text, 'html.parser')
    all_links = bs.find_all('a', id='video-title')
    print(all_links)

    pages = 0
    for links in all_links:
        bot.send_message(message.chat.id, links['href'])
        pages += 1
        if pages == 10:
            break


####################################################################################
@bot.message_handler(commands=['instagram'])
def instagram(message):
    bot.send_message(message.chat.id, 'Созадтель ссылок на инст')
    sleep(1)
    msg = bot.send_message(message.chat.id, 'Пришли мне ник юзера')
    bot.register_next_step_handler(msg, instagram_search)


def instagram_search(message):
    url = 'https://www.instagram.com/' + message.text
    bot.send_message(message.chat.id, url)


####################################################################################
@bot.message_handler(commands=['create_pass'])
def create_pass(message):
    print('[OK]')
    bot.send_message(message.chat.id, 'Генерация пароля')
    sleep(1)
    msg = bot.send_message(message.chat.id, 'Введите желаемую длину пароля: '
                                            '\n**Пароль не может быть меньше 6 символов**')

    bot.register_next_step_handler(msg, generate_password)


def generate_password(message):
    try:
        value = int(message.text)
    except:
        msg = bot.send_message(message.chat.id, 'Укажите число!')
        create_pass(msg)

    if value < 6:
        value = 6

    letters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!@$%&*:"?'
    letters_arr = [_ for _ in letters]
    password_arr = []

    index = 0
    while index != value:
        password_arr.append(random.choice(letters_arr))
        index += 1

    password = ''.join(password_arr)
    bot.send_message(message.chat.id, f'Ваш пароль:  {password}')


bot.polling()
