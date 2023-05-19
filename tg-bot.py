import telebot
import requests
from bs4 import BeautifulSoup

# токен бота
TOKEN = '6105600326:AAHOwfapbAaoncojjB8UdkdjYtl1sjJ0DPU'

# ссылка на новостной сайт
URL = 'https://rtvi.com/news'

# функция для получения заголовков, времени и ссылок на новости
def get_news(num):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = soup.find_all('div', class_='arch-block')
    if num > len(news_list) or num < 1:
        return None
    else:
        news_list = news_list[:num]
        result = []
        for news in news_list:
            title = news.find('h2', class_='arch-title').text.strip()
            time = news.find('div', class_='date').text.strip()
            link_elem = news.find('a', href=True)
            link = link_elem['href']

            result.append({'title': title, 'time': time, 'link': link})
        # сортируем список новостей в обратном порядке по времени публикации
        sorted_news = sorted(result, key=lambda x: x['time'], reverse=False)
        return sorted_news

# создание объекта бота
bot = telebot.TeleBot(TOKEN)

# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Введите число от 1 до 10')

# обработчик команды /stop
@bot.message_handler(commands=['stop'])
def stop_message(message):
    bot.send_message(message.chat.id, 'Бот остановлен')
    bot.stop_polling()

# обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def text_message(message):
    try:
        num = int(message.text)
        news = get_news(num)
        if news:
            # выводим новости в обратном порядке по времени
            for n in news:
                bot.send_message(message.chat.id, f"{n['title']}\n{n['time']}\n{n['link']}\n\n")
        else:
            bot.send_message(message.chat.id, 'Ошибка')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка')

# запуск бота
bot.polling()