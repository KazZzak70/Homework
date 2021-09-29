class HistoryDict:

    HISTORY_SIZE = 10

    def __init__(self, dict_init: dict):
        self._current_dict = dict_init
        self._dict_history_list = list(self._current_dict.keys())

    def set_value(self, key, value):
        self._current_dict[key] = value
        self._dict_history_list.append(key)
        self._dict_history_list = self._dict_history_list[-HistoryDict.HISTORY_SIZE:]

    def get_history(self):
        return self._dict_history_list


# if __name__ == "__main__":
#     d = HistoryDict({"a": 42})
#     d.set_value("b", 43)
#     d.set_value("c", 44)
#     d.set_value("d", 45)
#     d.set_value("e", 46)
#     d.set_value("f", 47)
#     d.set_value("g", 48)
#     d.set_value("h", 49)
#     d.set_value("i", 50)
#     d.set_value("j", 51)
#     d.set_value("k", 52)
#     print(d.get_history(), d.get_history().__len__())
