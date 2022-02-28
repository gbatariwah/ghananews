from utils.helpers import fetch_page


class GhanaWeb:
    def __init__(self, urls):
        self.urls = urls

    def get_top_stories(self):

        categories = self.urls['categories']

        top_stories = [self.get_lead_story(category)
                       for category in categories]

        return top_stories

    def get_lead_story(self, category):

        category_page_url = f"{self.urls['base']}{category['link']}"

        category_page = fetch_page(category_page_url)

        top_story_tag = category_page.find('div', id='inner-lead-story')

        title = top_story_tag.find('h2').string
        link = f"{category_page_url}/{top_story_tag.a.get('href')}"

        category = category['name']

        return {'title': title, 'link': link, 'category': category}

    def get_latest_news_by_category(self, category_name):

        categories = self.urls['categories']

        category, = filter(lambda x: x['name'] == category_name, categories)

        category_page_url = f"{self.urls['base']}{category['link']}"

        category_page = fetch_page(category_page_url)
        list_tag = category_page.find('ul', id='load_headlines')

        headline_tags = list_tag.find_all('li')
        latest_category_news = []
        for tag in headline_tags:
            title = tag.find('p').string
            link = self.urls['base'] + tag.a.get('href')
            time_ago = f'{tag.a.span.string} ago'

            item = {'title': title, 'link': link, 'time_ago': time_ago}

            latest_category_news.append(item)

        return latest_category_news[:11]


