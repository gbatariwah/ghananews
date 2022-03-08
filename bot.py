import os
import sqlite3
import asyncio

from telebot import types, async_telebot
from portals.ghanaweb import GhanaWeb
from portals.myjoyonline import MyJoyOnline
from portals.peacefmonline import PeaceFmOnline
from portals.tv3news import Tv3News
from urls.links import URLS
from utils.markups import category_markup, portals_markup
from dotenv import load_dotenv
from utils.queries import insert_user, create_users_table
import logging

ghanaweb = GhanaWeb(URLS['ghanaweb'])
myjoyonline = MyJoyOnline(URLS['myjoyonline'])
peacefmonline = PeaceFmOnline(URLS['peacefmonline'])
tv3news = Tv3News(URLS['tv3news'])
load_dotenv()

API_KEY = os.getenv('API_KEY')

bot = async_telebot.AsyncTeleBot(API_KEY)
db_connection = sqlite3.connect('database.db')

cursor = db_connection.cursor()

cursor.execute(create_users_table)
db_connection.commit()

# telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    m = message
    id = m.from_user.id
    username = m.from_user.username
    fname = m.from_user.first_name
    lname = m.from_user.last_name
    sdate = m.date
    user = (id, fname, lname, username, sdate)

    cursor.execute(insert_user, user)
    db_connection.commit()

    await bot.reply_to(message, """\
Hi {}, I am Ghana News bot.
I am here to help you get the latest news from Ghana!

 ➊ /portals - Menu
 ➋ /ghanaweb - News from GhanaWeb
 ➌ /myjoyonline - News from MyJoyOnline
 ➍ /peacefmonline - News from PeaceFmOnline
 
 📢 More updates coming!
 
 Developed by @geraldo09 ☄
 
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
        stories = [f"❀ {category.title()} {'' if category == 'news' or category == 'opinion' else 'News'} ❀"]
        headlines = myjoyonline.get_latest_news_by_category(category)

        for item in headlines:
            if item.get('section_label'):
                stories.append(f"❀❀ {item['section_label']} ❀❀")

            else:
                stories.append(f"{item['title']}\n{item['link']}\n")

    for o in stories:
        await bot.send_message(message.chat.id, text=o, reply_markup=markup)


@bot.message_handler(func=lambda message: '(T)' in message.text)
@bot.message_handler(commands=['3news'])
async def send_headlines2(message):
    portal_id = '(T)'
    # category = message.text.split(' ')[0].replace('/', '')
    # markup = category_markup(portal_id)
    items = tv3news.get_top_stories()
    stories = []

    if '3news' in message.text:
        pass
        # top_story = headlines['top_story']
        # news = headlines['news']
        #
        #
        for item in items:
            if item.get('category_name'):
                item_string = f"❀ {item['category_name']} ❀\n➿➿➿➿➿➿➿➿➿\n{item['title']}\n{item['link']}\n{item['date']}"
            else:
                item_string = f"{item['title']}\n{item['link']}\n"

            stories.append(item_string)

    else:
        pass
        # stories = [f"❀ {category.title()} {'' if category == 'news' or category == 'opinion' else 'News'} ❀"]
        # headlines = myjoyonline.get_latest_news_by_category(category)
        #
        # for item in headlines:
        #     if item.get('section_label'):
        #         stories.append(f"❀❀ {item['section_label']} ❀❀")
        #
        #     else:
        #         stories.append(f"{item['title']}\n{item['link']}\n")

    for o in stories:
        await bot.send_message(message.chat.id, text=o)


@bot.message_handler(func=lambda message: '(P)' in message.text)
@bot.message_handler(commands=['peacefmonline'])
async def send_headlines2(message):
    portal_id = '(P)'
    category = message.text.split(' ')[0].replace('/', '')
    markup = category_markup(portal_id)
    top_stories = peacefmonline.get_top_stories()

    if 'peacefmonline' in message.text:

        stories = []

        for story in top_stories:

            if story.get('excerpt'):
                story_string = f"{story['title']}\n➿➿➿➿➿➿➿➿\n{story['excerpt']}\n{story['link']}\n"

            else:
                if story.get('category_name'):
                    story_string = f"{story['category_name']}\n➿➿➿➿➿➿➿➿\n{story['title']}\n{story['link']}\n"
                else:
                    story_string = f"{story['title']}\n{story['link']}\n"

            stories.append(story_string)

    else:
        stories = [f"❀ {category.title()}  ❀"]
        headlines = peacefmonline.get_latest_news_by_category(category)

        for item in headlines:
            stories.append(f"{item['title']}\n{item['link']}\n\n{item['date']}")

    for o in stories:
        await bot.send_message(message.chat.id, text=o, reply_markup=markup)


@bot.message_handler(commands=['close'])
async def send_headlines2(message):
    markup = types.ReplyKeyboardRemove(selective=False)

    await bot.send_message(message.chat.id, text='➿➿➿➿ End ➿➿➿➿', reply_markup=markup)


@bot.message_handler(commands=['portals'])
async def send_headlines2(message):
    markup = portals_markup()
    await bot.send_message(message.chat.id, 'Choose a portal', reply_markup=markup)


# db_connection.close()

asyncio.run(bot.infinity_polling())
