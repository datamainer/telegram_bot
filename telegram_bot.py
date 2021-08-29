import telebot
from bs4 import BeautifulSoup
import requests
from time import sleep

TOKEN = '1982714627:AAGxOtxmSnOcXcwYAtA0sDqt-TSBfCEmaUs'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '''
>> Hey!
    
search engine{
..../avito
..../youtube
}

link creator{
..../instagram
}
''')


#########################################
@bot.message_handler(commands=['avito'])
def avito(message):
    bot.send_message(message.chat.id, '>> avito search')
    sleep(1)
    msg = bot.send_message(message.chat.id, '>> enter query: ')
    bot.register_next_step_handler(msg, avito_search)


def avito_search(message):
    url = 'https://www.avito.ru/petrozavodsk?q=' + message.text
    request = requests.get(url)
    bs = BeautifulSoup(request.text, 'html.parser')
    all_links = bs.find_all('a', class_='title-root-j7cja')

    pages = 0
    for link in all_links:
        links = 'https://www.avito.ru' + link['href']
        bot.send_message(message.chat.id, links)
        pages += 1
        if pages == 10:
            break


##########################################
@bot.message_handler(commands=['youtube'])
def youtube(message):
    bot.send_message(message.chat.id, '>> youtube search')
    sleep(1)
    msg = bot.send_message(message.chat.id, '>> enter query: ')
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


##########################################
@bot.message_handler(commands=['instagram'])
def instagram(message):
    bot.send_message(message.chat.id, '>> link creator ')
    sleep(1)
    msg = bot.send_message(message.chat.id, '>> enter nickname')
    bot.register_next_step_handler(msg, instagram_search)


def instagram_search(message):
    url = 'https://www.instagram.com/' + message.text
    bot.send_message(message.chat.id, url)


bot.polling()