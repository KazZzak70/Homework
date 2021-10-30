import requests


class ResultDataFileError(FileNotFoundError):
    pass


class UrlError(requests.RequestException):
    pass


class LimitError(ValueError):
    pass
