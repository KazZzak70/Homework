class ItemNotFoundError(AttributeError):
    pass


class ResultDataFileError(MemoryError, FileNotFoundError, FileExistsError):
    pass
