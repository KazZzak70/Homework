import re
from math import ceil


class Pagination:

    def __init__(self, text: str, maximum_page_size: int):
        self._text = text
        self._maximum_page_size = maximum_page_size

    def page_count(self):
        return ceil(self._text.__len__() / self._maximum_page_size)

    def item_count(self):
        return self._text.__len__()

    def count_items_on_page(self, page: int):
        if page == self.page_count() - 1:
            amount_of_items_on_page = self._text.__len__() - page * self._maximum_page_size
        elif page not in range(0, self.page_count()):
            raise Exception("Invalid index. Page is missing.")
        else:
            amount_of_items_on_page = self._maximum_page_size
        return amount_of_items_on_page

    def find_page(self, find_str: str):
        text = self._text
        result = list()
        for x in re.finditer(find_str, text):
            result.extend([y//self._maximum_page_size for y in range(x.start(), x.start() + find_str.__len__(), self._maximum_page_size)])
        if not result:
            raise Exception(f"'{find_str} is missing on the pages")
        return result

    def display_page(self, page: int) -> str:
        return self._text[page * self._maximum_page_size:(page+1) * self._maximum_page_size]


# if __name__ == "__main__":
#     book = Pagination("Your beautiful text", 5)
#     print(book.find_page("e"))
