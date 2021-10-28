import unittest
import date_converter


class TestDateConverter(unittest.TestCase):

    def test_check_user_date(self):
        user_date_cases = [202112345, 20221028, 20211310, 20211033, 20211131, 20210231]
        for date_case in user_date_cases:
            with self.assertLogs(level="ERROR") as cm:
                self.assertRaises(SystemExit, lambda: date_converter.check_user_date(date=date_case))
            self.assertEqual(cm.output, ['ERROR:root:Wrong date!'])

    def test_configure_the_date(self):
        date_cases = ["Wed, 27 Oct 2021 18:19:01 +0300", "2021-10-27T01:40:48Z"]
        expected_result = [20211027, 20211027]
        received_result = list()
        for date in date_cases:
            received_result.append(date_converter.configure_the_date(date))
        self.assertEqual(expected_result, received_result)
