from args import configure_parser
import unittest


class TestArgs(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = configure_parser()

    def test_args(self):
        test_case = ["--json", "True"]
        parsed = self.parser.parse_args(test_case)
        self.assertEqual(parsed.json, True)
