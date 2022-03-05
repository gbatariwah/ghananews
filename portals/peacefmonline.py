from utils.helpers import fetch_page


class PeaceFmOnline:
    def __init__(self, urls):
        self.urls = urls

    def get_top_stories(self):
        home_page = fetch_page(self.urls['base'])

        wrapper_tag = home_page.find('div', class_='jeg_wrapper wpb_wrapper')
        lead_story_content_tag = wrapper_tag.find('div', class_='jeg_postblock_content')

        top_stories = []
        lead_story = {}

        lead_story_title_tag = lead_story_content_tag.find('a')

        lead_story_title = lead_story_title_tag.string
        lead_story_link = self.urls['base'] + lead_story_title_tag.get('href')
        lead_story_excerpt = lead_story_content_tag.find('p').string

        lead_story['title'] = lead_story_title
        lead_story['link'] = lead_story_link
        lead_story['excerpt'] = lead_story_excerpt

        top_stories.append(lead_story)

        local_stories_tags = wrapper_tag.select('.jeg_post, .jeg_pl_sm, .format-standard')[1:]

        for tag in local_stories_tags:
            content_tag = tag.find('div', class_='jeg_postblock_content')

            link_tag = content_tag.find('a')
            title = link_tag.string
            link = self.urls['base'] + link_tag.get('href')

            story = {'title': title, "link": link}
            top_stories.append(story)

        category_tags = home_page.select('div[data-unique="jnews_module_15_5_5ffbc8e984b17"]')
        for tag in category_tags:
            category_name = tag.find('h3', class_='jeg_block_title').find('a').string
            link_tag = tag.select('h3[property="headline"]')[0].find('a')
            title = link_tag.string
            link = self.urls['base'] + link_tag.get('href')

            lead_story = {'category_name': category_name, 'title': title, 'link': link}

            top_stories.append(lead_story)

            other_stories_tags = tag.select('.jeg_post, .jeg_pl_sm, .format-standard')[1:]

            for inner_tag in other_stories_tags:
                link_tag = inner_tag.find('h3').find('a')

                title = link_tag.string
                link = self.urls['base'] + link_tag.get('href')

                other_story = {'title': title, 'link': link}

                top_stories.append(other_story)

        return top_stories

    def get_latest_news_by_category(self, category_name):
        stories = []
        categories = self.urls['categories']
        category, = filter(lambda x: x['name'] == category_name, categories)

        category_page_url = f"{self.urls['base']}{category['link']}"

        category_page = fetch_page(category_page_url)

        top_story_tag = category_page.find('div', class_='jeg_postbig')
        link_tag = top_story_tag.find('h3').find('a')
        top_story_title = link_tag.string
        top_story_link = self.urls['base'] + link_tag.get('href')
        top_story_date = top_story_tag.find('div', class_='jeg_meta_date').find('a').getText().lstrip()

        stories.append({'title': top_story_title, 'link': top_story_link, 'date': top_story_date})

        other_stories_tags = category_page.select('div[data-unique="jnews_module_62_1_5e13327d90ac8"]')[0].find_all('article')

        for tag in other_stories_tags:
            link_tag = tag.find('h3').find('a')
            top_story_title = link_tag.string
            top_story_link = link_tag.get('href')
            top_story_date = tag.find('div', class_='jeg_meta_date').find('a').getText().strip()
            story = {'title': top_story_title, 'link': top_story_link, 'date': top_story_date}
            stories.append(story)

        return stories

