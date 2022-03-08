from utils.helpers import fetch_page


class Tv3News:
    def __init__(self, urls):
        self.urls = urls

    def get_top_stories(self):
        home_page = fetch_page(self.urls['base'])
        stories = []

        slide_tags = home_page.find('div', class_='td-slider').find_all('div', class_='td_module_slide')
        for slide_tag in slide_tags:
            link_tag = slide_tag.find('h3').find('a')
            title = link_tag.string
            link = link_tag.get('href')
            date = slide_tag.find('time', class_='entry-date updated td-module-date').string
            category = slide_tag.find('span', class_='slide-meta-cat').find('a').string

            stories.append({'title': title, 'link': link, 'date': date, 'category_name': category})

        other_slides_tags = home_page.find('div', id='tdi_17').find_all('div', class_='td-block-span12')

        for other_slides_tag in other_slides_tags:
            link_tag = other_slides_tag.find('h3').find('a')
            title = link_tag.string
            link = link_tag.get('href')
            date = other_slides_tag.find('time', class_='entry-date updated td-module-date').string

            stories.append({'title': title, 'link': link, 'date': date})

        general_news_tags = home_page.find('div', class_='vc_row tdi_28  wpb_row td-pb-row').find_all('div',
                                                                                                      class_='vc_column')
        # for general_news_tag in general_news_tags:
        #

        return stories

    def get_latest_news_by_category(self, category_name):
        pass
        #
        # categories = self.urls['categories']
        #
        # category, = filter(lambda x: x['name'] == category_name, categories)
        #
        # category_page_url = f"{self.urls['base']}{category['link']}"
        #
        # category_page = fetch_page(category_page_url)
        # list_tag = category_page.find('ul', id='load_headlines')
        #
        # headline_tags = list_tag.find_all('li')
        # latest_category_news = []
        # for tag in headline_tags:
        #     title = tag.find('p').string
        #     link = self.urls['base'] + tag.a.get('href')
        #     time_ago = f'{tag.a.span.string} ago'
        #
        #     item = {'title': title, 'link': link, 'time_ago': time_ago}
        #
        #     latest_category_news.append(item)
        #
        # return latest_category_news[:11]
