import re
import requests
from bs4 import BeautifulSoup
from wrappers import execution_time


class Parser:

    HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
               'accept': '*/*'}
    url_pattern = re.compile(r"https?://[a-zA-Z0-9_\-/~\.:]+")

    def __init__(self, *, url: str):
        self.url = url
        self.result_data_list = list()
        self.html = None
        self.soup = None

    def get_html(self):
        try:
            r = requests.get(url=self.url, headers=Parser.HEADERS)
            return r
        except Exception as e:
            print("[ERROR] Check the url link")
            print(e)

    def __iter__(self):
        self.item = None
        return self

    def __next__(self):
        if self.item is None:
            self.item = self.soup.find('item')
        else:
            self.item = self.item.find_next_sibling('item')
        if self.item is None:
            raise StopIteration
        else:
            return self.item

    @execution_time
    def get_content(self):
        self.soup = BeautifulSoup(self.html.text, "xml")
        print(f"Feed: {self.soup.find('title').text}")
        for item in self:
            new_item = {
                    "title": item.title.text if item.title is not None else None,
                    "description": item.description.text.strip() if item.description is not None else None,
                    "link": item.link.text if item.link is not None else None,
                    "pubdate": item.pubDate.text if item.pubDate is not None else None,
                    "links": {
                        1: f"{item.link.text if item.link is not None else None} (link)"
                    }
                }
            if item.enclosure in item:
                image_url_list = list()
                image_url_list.extend(Parser.url_pattern.findall(str(item.enclosure)))
                for key, image_url in enumerate(image_url_list):
                    new_item['links'][key+2] = f"{image_url} (image)"
            if item.find('media:content') is not None:
                image_str = str(item.find('media:content'))
                image_url_list = list()
                image_url_list.extend(Parser.url_pattern.findall(image_str))
                for key, image_url in enumerate(image_url_list):
                    new_item['links'][key+2] = f"{image_url} (image)"
            self.result_data_list.append(new_item)
            print(
                f"\nTitle: {new_item['title']}\n"
                f"Date: {new_item['pubdate']}\n"
                f"Link: {new_item['link']}\n"
                f"Description: {new_item['description']}\n\n\n"
                f"Links:"
            )
            for key, value in new_item['links'].items():
                print(f"{key}: {value}")
        print(self.result_data_list)

    def parse(self):
        self.html = Parser.get_html(self)
        if self.html.status_code == 200:
            Parser.get_content(self)
        else:
            raise Exception("[ERROR] HTML status code is not 200")


if __name__ == "__main__":
    lenta_url = "http://lenta.ru/rss/articles"
    yahoo_url = "https://news.yahoo.com/rss/"
    parse = Parser(url=lenta_url)
    parse.parse()
