import os

from telebot import types, async_telebot
from portals.ghanaweb import GhanaWeb
from portals.myjoyonline import MyJoyOnline
from urls.links import URLS
from utils.markups import category_markup
from dotenv import load_dotenv
import logging

ghanaweb = GhanaWeb(URLS['ghanaweb'])
myjoyonline = MyJoyOnline(URLS['myjoyonline'])
load_dotenv()

API_KEY = os.getenv('API_KEY')

bot = async_telebot.AsyncTeleBot(API_KEY)


# telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    print('A user stated using your bot')
    await bot.reply_to(message, """\
Hi {}, I am Ghana News bot.
I am here to help you read the latest news in Ghana!\
 Enter /portals to get the latest news from GhanaWeb and Myjoyonline
""".format(message.from_user.username))


@bot.message_handler(func=lambda message: '(G)' in message.text)
@bot.message_handler(commands=['ghanaweb'])
async def send_headlines(message):
    portal_id = '(G)'
    markup = category_markup(portal_id)

    category = message.text.split(" ")[0].replace('/', '')

    if 'ghanaweb' in category:
        stories = ghanaweb.get_top_stories()
        title = "Top Stories"
    else:
        stories = ghanaweb.get_latest_news_by_category(category)
        title = "Latest News" if 'news' in category else f"Latest {category.title()} News"

    output = [f'❀{title}❀\n']

    for story in stories:
        headline = f"{story['title']}\n{story['link']}\n{story['time_ago'] if not 'ghanaweb' in category else story['category']}\n"

        output.append(headline)

    for o in output:
        await bot.send_message(message.chat.id, text=o, reply_markup=markup)


@bot.message_handler(commands=['back'])
async def go_back(message):
    markup = category_markup()
    await bot.send_message(message.chat.id, text='➿➿➿➿➿➿➿➿➿', reply_markup=markup)


@bot.message_handler(func=lambda message: '(M)' in message.text)
@bot.message_handler(commands=['myjoyonline'])
async def send_headlines2(message):
    portal_id = '(M)'
    category = message.text.split(' ')[0].replace('/', '')
    markup = category_markup(portal_id)
    headlines = myjoyonline.get_top_stories()

    if 'myjoyonline' in message.text:
        top_story = headlines['top_story']
        news = headlines['news']

        stories = [f"❀ Top Story ❀\n\n{top_story['title']}\n{top_story['link']}\n", "❀ News ❀"]

        for news_item in news:
            news_item_string = f"{news_item['title']}\n{news_item['link']}\n"

            stories.append(news_item_string)

    else:
        stories = [f"❀ {category.title()} {'' if category == 'news' or category =='opinion' else 'News'} ❀"]
        headlines = myjoyonline.get_latest_news_by_category(category)

        for item in headlines:
            if item.get('section_label'):
                stories.append(f"❀❀ {item['section_label']} ❀❀")

            else:
                stories.append(f"{item['title']}\n{item['link']}\n")

    for o in stories:
        await bot.send_message(message.chat.id, text=o, reply_markup=markup)


@bot.message_handler(commands=['close'])
async def send_headlines2(message):
    markup = types.ReplyKeyboardRemove(selective=False)

    await bot.send_message(message.chat.id, text='➿➿➿➿ End ➿➿➿➿', reply_markup=markup)


@bot.message_handler(commands=['portals'])
async def send_headlines2(message):
    markup = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, selective=False)
    btn1 = types.KeyboardButton('/ghanaweb')
    btn2 = types.KeyboardButton('/myjoyonline')
    btn3 = types.KeyboardButton('/close')
    markup.add(btn1, btn2, btn3)
    await bot.send_message(message.chat.id, 'Choose a portal', reply_markup=markup)


import asyncio

asyncio.run(bot.infinity_polling())
