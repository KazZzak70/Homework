class Money:

    _EXCHANGE_RATE = {"EUR": 0.93, "BYN": 2.1, "JPY": 110.86, "USD": 1}

    def __init__(self, value: [int, float], currency: str = "USD"):
        self.value = value
        self.currency = currency
        self.default_currency_value = self.default_currency_amount()

    def default_currency_amount(self) -> float:
        return float(self.value / self._EXCHANGE_RATE[self.currency])

    def __str__(self):
        return f"{self.value} {self.currency}"

    def __add__(self, other):
        if isinstance(other, Money):
            result_value = float(
                other.default_currency_value * Money._EXCHANGE_RATE[self.currency] + self.value)
            result_currency = self.currency
            return Money(result_value, result_currency)
        else:
            raise TypeError("Expected class Money()")

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Money):
            result_value = float(
                other.default_currency_value * Money._EXCHANGE_RATE[self.currency] - self.value)
            result_currency = self.currency
            return Money(result_value, result_currency)
        else:
            raise TypeError("Expected class Money()")

    def __rmul__(self, other):
        if isinstance(other, float):
            result_value = float(other * self.value)
            return Money(result_value, self.currency)

    def __mul__(self, other):
        if isinstance(other, float):
            result_value = float(other * self.value)
            return Money(result_value, self.currency)

    def __truediv__(self, other: [int, float]):
        result_value = float(self.value / other)
        return Money(result_value, self.currency)

    def __eq__(self, other):
        if isinstance(other, Money):
            return self.default_currency_value == other.default_currency_value
        else:
            raise TypeError("Expected class Money()")

    def __lt__(self, other):
        if isinstance(other, Money):
            return self.default_currency_value < other.default_currency_value
        else:
            raise TypeError("Expected class Money()")


# if __name__ == "__main__":
#     lst = [Money(10, "BYN"), Money(11), Money(12.01, "JPY")]
#     s = sum(lst)
#     print(s)
