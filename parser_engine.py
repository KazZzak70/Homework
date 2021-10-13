import re
from time import sleep
import requests
from bs4 import BeautifulSoup
from wrappers import execution_time
from pprint import pprint
import logging
import sys


class ItemNotFoundError(AttributeError):
    pass


class Parser:

    HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
               'accept': '*/*'}
    url_pattern = re.compile(r"https?://[a-zA-Z0-9_\-/~\.:]+")

    def __init__(self, *, url: str, stdout_json: bool, stdout_verbose: bool, limit: int):
        self.url = url
        self.result_data_list = list()
        self.html = None
        self.soup = None
        self.feed = None
        self.total_items = None
        self.stdout_json = stdout_json
        self.stdout_verbose = stdout_verbose
        self.limit_amount = limit
        self.configure_logger()

    def __iter__(self):
        self.item = None
        self.total_items = self.soup.find_all("item").__len__()
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

    # TODO Вынести обработку исключений в декоратор
    def get_html(self):
        if self.stdout_verbose:
            logging.info(msg=f"Sending a get request to {self.url}")
        try:
            response = requests.get(url=self.url, headers=Parser.HEADERS)
            response.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            logging.error(msg="Timed out.")
        except requests.exceptions.ConnectionError:
            logging.error(msg=f"HTTP Connection error, max retries exceeded")
        except requests.exceptions.HTTPError as err:
            logging.error(msg=f"{err}")
        except requests.exceptions.ReadTimeout as err:
            logging.error(msg=f"{err}")
        else:
            if self.stdout_verbose:
                logging.info(msg=f"Status code is {response.status_code}")
            return response

    def configure_logger(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if self.stdout_verbose else logging.ERROR)

    @staticmethod
    def get_all_urls(item):
        url_list = list()
        if item.enclosure is not None:
            url_list.extend(Parser.url_pattern.findall(str(item.enclosure)))
        elif item.find("media:content") is not None:
            url_list.extend(Parser.url_pattern.findall(str(item.find("media:content"))))
        return url_list

    def get_content(self):
        self.soup = BeautifulSoup(self.html.text, "xml")
        self.feed = self.soup.find('title').text
        if self.feed:
            print(f"\nFeed: {self.feed}")
        if self.stdout_verbose:
            logging.info(msg=f"Starting collecting items")
        iteration = 0
        for item in self:
            try:
                iteration += 1
                if iteration == self.limit_amount:
                    break
                new_item = {
                        "title": item.title.text if item.title is not None else None,
                        "description": item.description.text.strip() if item.description is not None else None,
                        "link": item.link.text if item.link is not None else None,
                        "pubdate": item.pubDate.text if item.pubDate is not None else None,
                        "links": {
                            1: f"{item.link.text if item.link is not None else None} (link)"
                        }
                    }
                url_list = self.get_all_urls(item)
                if url_list:
                    for key, url in enumerate(url_list):
                        new_item['links'][key+2] = f"{url} (image)"
                if self.stdout_verbose:
                    logging.info(msg=f"Item {iteration} received")
                self.result_data_list.append(new_item)
            except ItemNotFoundError:
                raise ItemNotFoundError('Item tag not found.')

    def data_output(self):
        if self.stdout_json:
            pprint(self.result_data_list)
        else:
            for item in self.result_data_list:
                print(f"\n--------------------------------------------------------------------------------------------")
                if item['title']:
                    print(f"Title: {item['title']}")
                if item['pubdate']:
                    print(f"Date: {item['pubdate']}")
                if item['link']:
                    print(f"Link: {item['link']}")
                if item['description']:
                    print(f"Description: {item['description']}")
                if item['links']:
                    print(f"\n\nLinks:")
                    for key, url in item['links'].items():
                        print(f"[{key}]: {url}")

    @execution_time
    def parse(self):
        html = Parser.get_html(self)
        self.html = html if html is not None else exit()
        if self.html.status_code == 200:
            Parser.get_content(self)
            Parser.data_output(self)


if __name__ == "__main__":
    lenta_url = "http://lenta.ru/rss/articles"
    yahoo_url = "https://news.yahoo.com/rss/"
    test_url = "http://httpbin.org/delay/10"
    parse = Parser(url=yahoo_url, stdout_json=False, stdout_verbose=True, limit=0)
    parse.parse()
