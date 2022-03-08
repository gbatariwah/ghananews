from urls.links import URLS
import os

from dotenv import load_dotenv

load_dotenv()

key = os.getenv('API_KEY')

from portals.tv3news import Tv3News


tv3news = Tv3News(URLS['tv3news'])


print(tv3news.get_top_stories())


