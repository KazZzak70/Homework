from fb2_output import output_data_fb2
from pdf_output import output_data_pdf
from date_converter import configure_the_date
from bs4 import BeautifulSoup
import exceptions
import wrappers
import requests
import logging
import pathlib
import pprint
import json
import sys
import re


class Parser:
    """
    This class is used for parsing RSS channels version 2.0.
    """

    HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
               'accept': '*/*'}
    OUTPUT_DATA_PATH = pathlib.Path(pathlib.Path.cwd(), "output_data")
    url_pattern = re.compile(r"https?://[a-zA-Z0-9_\-/~\.:]+")

    def __init__(self):
        """
        This is a class constructor.

        :rtype: object
        """
        self.soup = None
        self.item = None

    def __iter__(self):
        """
        This method implements a class object as an iterable object.

        :rtype: object
        """
        return self

    def __next__(self):
        """
        This method implements getting the next item.

        :return: A PageElement
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
        if self.item is None:
            self.item = self.soup.find('item')
        else:
            self.item = self.item.find_next_sibling('item')
        if self.item is None:
            raise StopIteration
        else:
            return self.item

    @wrappers.execution_time
    def __call__(self, *, url: str, stdout_json: bool, stdout_verbose: bool, limit: int, date: int, pdf: bool,
                 fb2: bool):
        """
        This method is an implementation of calling an class instance a function.

        :param url: URL to the RSS channel
        :type url: str
        :param stdout_json: flag about the need to output data in JSON-format
        :type stdout_json: bool
        :param stdout_verbose: flag about the need to display additional information during execution
        :type stdout_verbose: bool
        :param limit: number of news in the output
        :type limit: int
        :param date: Sort news for a given date
        :type date: int

        :rtype: object
        """
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if stdout_verbose else logging.ERROR)
        if url is None and date is None:
            logging.error(msg="So, what should I do?")
            exit()
        if url is None and date is not None:
            json_files_list = Parser.get_json_files_list()
            Parser.sort_by_date(json_files_list=json_files_list, date=date, verbose_flag=stdout_verbose,
                                json_flag=stdout_json, limit=limit)
            if pdf:
                for json_file in json_files_list:
                    file_path = pathlib.Path(Parser.OUTPUT_DATA_PATH, json_file)
                    output_data_pdf(file_path, date, limit)
            if fb2:
                for json_file in json_files_list:
                    file_path = pathlib.Path(Parser.OUTPUT_DATA_PATH, json_file)
                    output_data_fb2(file_path, date, limit)
        if url is not None and date is not None:
            file_name = Parser.generate_result_file_name(url)
            Parser.sort_by_date(json_files_list=[file_name], date=date, verbose_flag=stdout_verbose,
                                json_flag=stdout_json, limit=limit)
            file_path = pathlib.Path(Parser.OUTPUT_DATA_PATH, file_name)
            if pdf:
                output_data_pdf(file_path, date, limit)
            if fb2:
                output_data_fb2(file_path, date, limit)
        if url is not None and date is None:
            html = Parser.get_html(url=url, verbose_flag=stdout_verbose)
            html = html if html is not None else exit()
            if html.status_code == 200:
                result_file_name = Parser.generate_result_file_name(url=url)
                result_file_path = pathlib.Path(Parser.OUTPUT_DATA_PATH, result_file_name)
                src_data = Parser.get_content(self, html=html.text, verbose_flag=stdout_verbose)
                with open(result_file_path, 'w') as export_file:
                    Parser.export_content(file=export_file, src_data=src_data, verbose_flag=stdout_verbose)
                try:
                    with open(result_file_path) as src_file:
                        src = json.load(src_file)
                    Parser.data_output(src_data=src, verbose_flag=stdout_verbose, json_flag=stdout_json, limit=limit)
                except exceptions.ResultDataFileError as _ex:
                    logging.error(msg="Result data file error")
                    exit()
                if pdf:
                    output_data_pdf(result_file_path, limit=limit)
                if fb2:
                    output_data_fb2(result_file_path, limit=limit)

    @staticmethod
    def sort_by_date(json_files_list: list, date: int, verbose_flag: bool, json_flag: bool, limit: int):
        for file in json_files_list:
            file_path = pathlib.Path(Parser.OUTPUT_DATA_PATH, file)
            try:
                with open(file_path) as src_file:
                    src = json.load(src_file)
                Parser.data_output(src_data=src, verbose_flag=verbose_flag, json_flag=json_flag, date=date, limit=limit)
            except (exceptions.ResultDataFileError, FileNotFoundError) as _ex:
                if len(json_files_list) == 1:
                    logging.error(msg="Not found data from this URL in local memory")
                else:
                    logging.error(msg="Result data file error")

    def check_the_link_type(self):
        if not self.soup.find("rss"):
            logging.error(msg="This is not RSS link")
            exit()

    @staticmethod
    def get_json_files_list():
        json_files_list = [file.name for file in Parser.OUTPUT_DATA_PATH.iterdir() if
                           file.is_file() and file.name.endswith(".json")]
        return json_files_list

    @staticmethod
    def generate_result_file_name(url: str) -> str:
        begin_pattern = re.compile(r"https?://")
        match = begin_pattern.search(url)
        result_name = f'{url[match.end():].replace("/", "_").replace(".", "_")}.json'
        return result_name

    @staticmethod
    @wrappers.network_exceptions_catcher
    def get_html(*, url: str, verbose_flag: bool, **kwargs):
        """
        This method is implements sending a get request to URL.

        :param url: URL to the RSS channel
        :type url: str
        :param verbose_flag: flag about the need to display additional information during execution
        :type verbose_flag: bool

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        if verbose_flag:
            logging.info(msg=f"Sending a get request to {url}")
        response = requests.get(url=url, headers=Parser.HEADERS, **kwargs)
        if verbose_flag:
            logging.info(msg=f"Status code is {response.status_code}")
        return response

    @staticmethod
    def get_all_urls(item) -> list[str]:
        """
        This method implements a search for all links using a regular expression.

        :param item: bs4.element.Tag | bs4.element.NavigableString

        :rtype: list
        """
        url_list = list()
        if item.enclosure is not None:
            url_list.extend(Parser.url_pattern.findall(str(item.enclosure)))
        elif item.content is not None:
            url_list.extend(Parser.url_pattern.findall(str(item.content)))
        return url_list

    def get_content(self, *, html: str, verbose_flag: bool) -> dict:
        """
        This method implements the formation of an output dictionary with news data.

        :param html: .text attribute of :class:`Response <Response>` object
        :type html: str
        :param verbose_flag: flag about the need to display additional information during execution
        :type verbose_flag: bool

        :raise exceptions.ItemNotFoundError: if there is no .item attribute
            in bs4.element.Tag | bs4.element.NavigableString

        :return: dict with collected data
        :rtype: dict
        """
        self.soup = BeautifulSoup(html, "xml")
        self.check_the_link_type()
        feed = self.soup.find('title').text
        if verbose_flag:
            logging.info(msg=f"Starting collecting items")
        result_data = {'feed': feed, 'items': list()}
        for item in self:
            new_item = {
                "title": item.title.text if item.title is not None else None,
                "description": item.description.text.strip() if item.description is not None else None,
                "link": item.link.text if item.link is not None else None,
                "pubdate": configure_the_date(item.pubDate.text) if item.pubDate is not None else None,
                "links": {
                    "1": item.link.text if item.link is not None else None
                }
            }
            url_list = Parser.get_all_urls(item)
            if url_list:
                for key, url in enumerate(url_list):
                    new_item["links"][str(key + 2)] = url
            result_data["items"].append(new_item)
        return result_data

    @staticmethod
    def export_content(*, file, src_data, verbose_flag: bool):
        """
        This method implements outputting data to a json file.

        :param file:
        :type file: :class: '_io.TextIOWrapper'
        :param src_data: collected data
        :param verbose_flag: flag about the need to display additional information during execution
        :type verbose_flag: bool
        """
        json.dump(src_data, file, indent=4, ensure_ascii=False)
        if verbose_flag:
            logging.info(msg=f'Saving result data file to {str(pathlib.Path(__file__).parent.resolve())}')

    @staticmethod
    def data_output(*, src_data: dict, verbose_flag: bool, json_flag: bool, limit: int, date: int = None):
        """
        This method implements data output to stdout in the selected format.

        :param src_data: dictionary with initial data for output
        :type src_data: dict
        :param verbose_flag: flag about the need to display additional information during execution
        :type verbose_flag: bool
        :param json_flag: flag about the need to output data in JSON-format
        :type json_flag: bool
        :param date: Sort news for a given date
        :type date: int
        :param limit: number of news in the output
        :type limit: int

        :raise exceptions.ResultDataFileError: if there are problems with memory,
            file name or file path or file don't exist
        """
        iteration = 0
        exists_flag = False
        print(f"\nFeed: {src_data['feed']}")
        if json_flag:
            if limit is not None and limit <= 20:
                for item in src_data['items']:
                    if (date is not None and item["pubdate"] == date) or date is None:
                        print()
                        iteration += 1
                        pprint.pprint(f"{item}\n")
                        exists_flag = True
                        if iteration == limit:
                            break
            else:
                for item in src_data['items']:
                    if (date is not None and item["pubdate"] == date) or date is None:
                        print()
                        iteration += 1
                        print(item, end='\n\n')
                        exists_flag = True
                        if iteration == limit:
                            break
        else:
            for item in src_data['items']:
                if (date is not None and item["pubdate"] == date) or date is None:
                    print()
                    iteration += 1
                    exists_flag = True
                    for key in item.keys():
                        if key == 'links':
                            print(f"{key.capitalize()}:")
                            for dict_key, dict_value in item[key].items():
                                print(f"[{dict_key}]: {dict_value}")
                        else:
                            if item[key] is not None:
                                print(f"{key.capitalize()}: {item[key]}")
                    if iteration == limit:
                        break
        if not exists_flag:
            print(f"There are no news for the chosen date")
        if verbose_flag:
            print(f"Total amount of collected items in local memory is {len(src_data['items'])}")


if __name__ == "__main__":
    lenta_url = "http://lenta.ru/rss/articles"
    yahoo_url = "https://news.yahoo.com/rss/"
    aif_url = "https://aif.ru/rss/politics.php"
    test_url = "http://httpbin.org/delay/10"
