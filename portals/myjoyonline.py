from utils.helpers import fetch_page


class MyJoyOnline:
    def __init__(self, urls):
        self.urls = urls

    def get_top_stories(self):
        home_page = fetch_page(self.urls['base'])

        top_story_tag = home_page.find('div', class_='col-md-6 col-xs-12 col-lg-12 col-xl-8')
        top_story_link = top_story_tag.find('div', class_='img-holder').a.get('href')
        top_story_title = top_story_tag.find('h1').string

        top_story = {
            'title': top_story_title,
            'link': top_story_link,
            'label': 'top story'
        }

        news = []

        news_tags = home_page.find_all('div', class_='col-lg-6 col-sm-6 col-md-6 col-xs-12 mt-3')

        for tag in news_tags:
            title = tag.find('h4').string
            link = tag.find('div', class_='home-post-list-title').a.get('href')

            news_item = {
                'title': title,
                'link': link
            }

            news.append(news_item)

        return {
            'top_story': top_story,
            'news': news
        }

    def get_latest_news_by_category(self, category_name):
        categories = self.urls['categories']
        category, = filter(lambda x: x['name'] == category_name, categories)

        category_page_url = f"{self.urls['base']}{category['link']}"

        category_page = fetch_page(category_page_url)

        top_stories_tags = category_page.find('div', class_='col-md-12 col-xs-12 col-lg-12').div.div.contents

        top_stories = []

        for tag in top_stories_tags:
            if tag is not None:
                title = tag.find('h1').string
                link = tag.find('a').get('href')

                top_stories.append({'title': title, 'link': link})

        other_stories = []

        other_stories_tags = category_page.find(
            'div', class_='col-sm-12 col-md-12 col-lg-9 mt-lg-3 mt-sm-3 mt-md-3').div.contents

        for tag in other_stories_tags:

            has_class = tag.attrs.get('class') is not None

            if has_class:
                is_section_label = tag.attrs.get('class')[0] == 'col-lg-12'
                is_opinion_tag = tag.attrs.get('class')[0] == 'col-lg-3'

                print(is_opinion_tag)
                if is_section_label:
                    if category_name != 'opinion':
                        label = tag.find('h4').string
                        other_stories.append({'section_label': label})
                else:
                    title = tag.find('h4').string
                    link = tag.find('a').get('href')
                    other_stories.append({'title': title, 'link': link})

        top_stories += other_stories

        return top_stories
