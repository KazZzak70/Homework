from unittest.mock import patch
from pdf_output.pdf_output import generate_a_row, link_separator, get_data_list
import unittest


class TestPdfOutput(unittest.TestCase):

    def setUp(self) -> None:
        self.max_line_len = 25
        self.test_row = "Bill Belichick reportedly gives hard-working, underpaid Patriots coaches"
        self.header_name = "description"
        self.link = "https://news.yahoo.com/bill-belichick-reportedly-gives-hard-150359034.html"

    def test_generate_a_row_online_mode(self):
        expected_result = [[" ", self.header_name, "Bill Belichick reportedly"], [" ", " ", "gives hard-working,"],
                           [" ", " ", "underpaid Patriots"], [" ", " ", "coaches"]]
        received_result = generate_a_row(row_content=self.test_row, header_name=self.header_name,
                                         max_line_len=self.max_line_len, online_mode_flag=True)
        self.assertEqual(expected_result, received_result)

    def test_generate_a_row_offline_mode(self):
        expected_result = [[self.header_name, "Bill Belichick reportedly"], [" ", "gives hard-working,"],
                           [" ", "underpaid Patriots"], [" ", "coaches"]]
        received_result = generate_a_row(row_content=self.test_row, header_name=self.header_name,
                                         max_line_len=self.max_line_len, online_mode_flag=False)
        self.assertEqual(expected_result, received_result)

    def test_generate_a_row_short_case_online(self):
        expected_result = [[" ", self.header_name, "Bill Belichick "]]
        received_result = generate_a_row(row_content=self.test_row[:15], header_name=self.header_name,
                                         max_line_len=self.max_line_len, online_mode_flag=True)
        self.assertEqual(expected_result, received_result)

    def test_generate_a_row_short_case_offline(self):
        expected_result = [[self.header_name, "Bill Belichick "]]
        received_result = generate_a_row(row_content=self.test_row[:15], header_name=self.header_name,
                                         max_line_len=self.max_line_len, online_mode_flag=False)
        self.assertEqual(expected_result, received_result)

    def test_link_separator_online_mode(self):
        expected_result = [[" ", self.header_name, "https://news.yahoo.com/bi"],
                           [" ", " ", "ll-belichick-reportedly-g"],
                           [" ", " ", "ives-hard-150359034.html"]]
        received_result = link_separator(link=self.link, header_name=self.header_name,
                                         max_line_len=self.max_line_len, online_mode_flag=True)
        self.assertEqual(expected_result, received_result)

    def test_link_separator_offline_mode(self):
        expected_result = [[self.header_name, "https://news.yahoo.com/bi"],
                           [" ", "ll-belichick-reportedly-g"],
                           [" ", "ives-hard-150359034.html"]]
        received_result = link_separator(link=self.link, header_name=self.header_name,
                                         max_line_len=self.max_line_len, online_mode_flag=False)
        self.assertEqual(expected_result, received_result)

    def test_link_separator_short_case_online(self):
        expected_result = [[" ", self.header_name, "https://news.yahoo.com/"]]
        received_result = link_separator(link=self.link[:23], header_name=self.header_name,
                                         max_line_len=self.max_line_len, online_mode_flag=True)
        self.assertEqual(expected_result, received_result)

    def test_link_separator_short_case_offline(self):
        expected_result = [[self.header_name, "https://news.yahoo.com/"]]
        received_result = link_separator(link=self.link[:23], header_name=self.header_name,
                                         max_line_len=self.max_line_len, online_mode_flag=False)
        self.assertEqual(expected_result, received_result)

    @patch("pdf_output.pdf_output.link_separator")
    @patch("pdf_output.pdf_output.generate_a_row")
    def test_get_data_list(self, generate_a_row_mock, link_separator_mock):
        online_mode_flag = False
        generate_a_row_mock.return_value = [["Title:", "Woman in Thailand's"], [" ", "high-rise cuts rope"],
                                            [" ", "holding painters"]]
        link_separator_mock.return_value = [
            ["Link:", "https://news.yahoo.com/wo"], [" ", "man-thailands-high-rise-c"], [" ", "uts-121706149.html"]]
        example_data = {
            "title": "Woman in Thailand's high-rise cuts rope holding painters",
            "description": None,
            "link": "https://news.yahoo.com/woman-thailands-high-rise-cuts-121706149.html",
            "pubdate": 20211027,
        }
        expected_result = [["Title:", "Woman in Thailand's"], [" ", "high-rise cuts rope"], [" ", "holding painters"],
                           ["Link:", "https://news.yahoo.com/wo"], [" ", "man-thailands-high-rise-c"],
                           [" ", "uts-121706149.html"], ["Pubdate:", 20211027]]
        received_result = get_data_list(item=example_data, online_mode=online_mode_flag,
                                        max_line_len=self.max_line_len)
        self.assertEqual(expected_result, received_result)
        generate_a_row_mock.assert_called_once()
        link_separator_mock.assert_called_once()
