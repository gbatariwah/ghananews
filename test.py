from urls.links import URLS
import os

from dotenv import load_dotenv

load_dotenv()

key = os.getenv('API_KEY')

from portals.peacefmonline import PeaceFmOnline


peacefmonline = PeaceFmOnline(URLS['peacefmonline'])


print(peacefmonline.get_latest_news_by_category('local'))


