from urls.links import URLS
import os

from dotenv import load_dotenv

load_dotenv()

key = os.getenv('API_KEY')

from portals.myjoyonline import MyJoyOnline


myjoyonline = MyJoyOnline(URLS['myjoyonline'])

# print(myjoyonline.get_latest_news_by_category('opinion'))

print(key)


