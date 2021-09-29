class Counter:

    def __init__(self, start=0, stop=None):
        self._current_value = start
        self._stop_value = stop

    def increment(self):
        if self._stop_value is not None and self._current_value >= self._stop_value:
            print("Maximum value is reached")
            return
        self._current_value += 1

    def get(self):
        return self._current_value


# if __name__ == "__main__":
#     c = Counter(start=42, stop=43)
#     c.increment()
#     print(c.get())
#     c.increment()
#     print(c.get())


