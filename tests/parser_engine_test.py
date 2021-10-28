from collections import Iterable
from parser_engine import Parser
from bs4 import BeautifulSoup
from unittest.mock import patch
from io import StringIO
from pathlib import Path
import unittest
import json
import io

FOLDER_PATH = Path(Path.cwd(), "test_snippets")


class TestParser(unittest.TestCase):
    FILE_SNIPPETS_NAMES_LIST = ["data_1_item.json", "data_1_json_mode", "data_1_normal_mode", "data_25_items.json",
                                "data_25_json_mode"]
    ITEM_NAMES_LIST = ["item_with_enclosure", "item_with_media_content", "one_item", "one_item.json"]
    FILE_SNIPPETS_PATH_LIST = [Path(FOLDER_PATH, file_name) for file_name in FILE_SNIPPETS_NAMES_LIST]
    ITEMS_PATH_LIST = [Path(FOLDER_PATH, item_name) for item_name in ITEM_NAMES_LIST]

    def setUp(self) -> None:
        self.test_instance = Parser()
        self.maxDiff = None
        self.stdout_verbose_mode = None
        self.stdout_json_mode = None
        self.stdout_limit = None
        self.test_items_list = list()
        for file_path in TestParser.ITEMS_PATH_LIST[:2]:
            with open(file_path) as src:
                self.test_items_list.append(BeautifulSoup(src.read(), "xml"))

    def test_get_all_urls(self):
        expected_result = [
            ["https://icdn.lenta.ru/images/2021/10/18/16/20211018162124502/pic_003be8c38c6663e8de08551bd6003f30.jpg"],
            ["https://s.yimg.com/os/creatr-uploaded-images/2021-10/b96d2a40-3032-11ec-affc-8609c7aa0cf2"]]
        received_result = list()
        for item in self.test_items_list:
            received_result.append(Parser.get_all_urls(item))
            self.assertEqual(list.__name__, Parser.get_all_urls(item).__class__.__name__)
        self.assertEqual(expected_result, received_result)

    def test_get_html_verbose_mode(self):
        test_url = "http://httpbin.org/status/200"
        expected_output = [
            f"INFO:root:Sending a get request to {test_url}",
            f"DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): "
            f"httpbin.org:80",
            f"DEBUG:urllib3.connectionpool:http://httpbin.org:80 \"GET /status/200 "
            f"HTTP/1.1\" 200 0",
            f"INFO:root:Status code is 200"
        ]
        with self.assertLogs(level="DEBUG") as cm:
            response = Parser.get_html(url=test_url, verbose_flag=True)
            self.assertEqual("Response", response.__class__.__name__)
        self.assertEqual(cm.output, expected_output)

    def test_get_html_connect_timeout(self):
        test_url = "http://httpbin.org/status/200"
        with self.assertLogs(level="ERROR") as cm:
            Parser.get_html(url=test_url, verbose_flag=False, timeout=0.01)
        self.assertEqual(cm.output, ["ERROR:root:Timed out."])

    def test_get_html_connection_error(self):
        test_url = "https://kdngsdtnvist.djklg"
        with self.assertLogs(level="ERROR") as cm:
            Parser.get_html(url=test_url, verbose_flag=False)
        self.assertEqual(cm.output, ["ERROR:root:HTTP Connection error, max retries exceeded"])

    def test_get_html_http_error(self):
        test_url = "http://httpbin.org/status/423"
        with self.assertLogs(level="ERROR") as cm:
            Parser.get_html(url=test_url, verbose_flag=False)
        self.assertEqual(cm.output, [f"ERROR:root:423 Client Error: LOCKED for url: {test_url}"])

    def test_get_html_read_timeout(self):
        test_url = "http://httpbin.org/delay/10"
        with self.assertLogs(level="ERROR") as cm:
            Parser.get_html(url=test_url, verbose_flag=False, timeout=1)
        self.assertEqual(cm.output, [
            "ERROR:root:HTTPConnectionPool(host='httpbin.org', port=80): Read timed out. (read timeout=1)"])

    def test_export_content_verbose_mode(self):
        outfile = StringIO()
        expected_data = {"feed": "some_feed", "items": []}
        with self.assertLogs(level="DEBUG") as cm:
            Parser.export_content(file=outfile, src_data=expected_data, verbose_flag=True)
        outfile.seek(0)
        received_data = json.load(outfile)
        self.assertDictEqual(expected_data, received_data)
        self.assertEqual(cm.output, ['INFO:root:Saving result data file to /home/maksim/MyProjects'])

    @patch("sys.stdout", new_callable=io.StringIO)
    def assertEqualStdout(self, src, expected_output, mock_stdout):
        Parser.data_output(src_data=src, verbose_flag=self.stdout_verbose_mode, json_flag=self.stdout_json_mode,
                           limit=self.stdout_limit)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_data_output_1_item_json_mode(self):
        self.stdout_json_mode = True
        self.stdout_verbose_mode = False
        with open(TestParser.FILE_SNIPPETS_PATH_LIST[0]) as src_file:
            src = json.load(src_file)
        with open(TestParser.FILE_SNIPPETS_PATH_LIST[1]) as output_file:
            expected_result = output_file.read()
        self.assertEqualStdout(src, expected_result)

    def test_data_output_1_item_normal_mode_verbose(self):
        self.stdout_json_mode = False
        self.stdout_verbose_mode = True
        with open(TestParser.FILE_SNIPPETS_PATH_LIST[0]) as src_file:
            src = json.load(src_file)
        with open(TestParser.FILE_SNIPPETS_PATH_LIST[2]) as output_file:
            expected_result = output_file.read()
        self.assertEqualStdout(src, expected_result)

    def test_data_output_25_items_json_mode(self):
        self.stdout_json_mode = True
        self.stdout_verbose_mode = False
        with open(TestParser.FILE_SNIPPETS_PATH_LIST[3]) as src_file:
            src = json.load(src_file)
        with open(TestParser.FILE_SNIPPETS_PATH_LIST[4]) as output_file:
            expected_result = output_file.read()
        self.assertEqualStdout(src, expected_result)

    def test_obj_is_iterable(self):
        self.test_instance.__iter__()
        self.assertIsInstance(self.test_instance, Iterable)

    def test_obj_generator_case_first_item(self):
        with open(TestParser.ITEMS_PATH_LIST[2]) as src_file:
            src = src_file.read()
        self.test_instance.soup = BeautifulSoup(src, "xml")
        expected_first_item = self.test_instance.soup.find("item")
        first_item = self.test_instance.__next__()
        self.assertEqual(first_item, expected_first_item)

    def test_obj_generator_case_last_item(self):
        with open(TestParser.ITEMS_PATH_LIST[2]) as src_file:
            src = src_file.read()
        self.test_instance.soup = BeautifulSoup(src, "xml")
        self.test_instance.item = self.test_instance.soup.find("item")
        with self.assertRaises(StopIteration):
            self.test_instance.__next__()

    @patch.object(Parser, "get_all_urls")
    def test_get_content(self, mock_get_all_urls):
        mock_get_all_urls.return_value = [
            "https://icdn.lenta.ru/images/2021/10/20/16/20211020160507876/pic_6416ef6b1cec76ad10417046923c1cef.jpg"]
        with open(TestParser.ITEMS_PATH_LIST[3]) as src_file:
            expected_result_dict = json.load(src_file)
        with open(TestParser.ITEMS_PATH_LIST[2]) as src_file:
            src = src_file.read()
        self.test_instance.soup = BeautifulSoup(src, "xml")
        received_dict = self.test_instance.get_content(html=src, verbose_flag=False)
        self.assertEqual(received_dict, expected_result_dict)
        mock_get_all_urls.assert_called_once()
        self.assertEqual(dict.__name__, received_dict.__class__.__name__)

    @patch.object(Parser, "get_all_urls")
    def test_get_content_verbose_mode(self, mock_get_all_urls):
        mock_get_all_urls.return_value = None
        with open(TestParser.ITEMS_PATH_LIST[2]) as src_file:
            src = src_file.read()
        self.test_instance.soup = BeautifulSoup(src, "xml")
        with self.assertLogs(level="DEBUG") as cm:
            self.test_instance.get_content(html=src, verbose_flag=True)
        self.assertEqual(cm.output, ["INFO:root:Starting collecting items"])

    def test_generate_result_file_name(self):
        url = "http://lenta.ru/rss/articles"
        expected_result = "lenta_ru_rss_articles.json"
        received_result = Parser.generate_result_file_name(url=url)
        self.assertEqual(expected_result, received_result)

    def test_check_the_link_type(self):
        self.test_instance.soup = BeautifulSoup("one-two-stop", "xml")
        with self.assertLogs(level="ERROR") as cm:
            self.assertRaises(SystemExit, lambda: Parser.check_the_link_type(self=self.test_instance))
        self.assertEqual(cm.output, ["ERROR:root:This is not RSS link"])


if __name__ == '__main__':
    unittest.main()
