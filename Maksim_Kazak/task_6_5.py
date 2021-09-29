class Singleton:

    instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Sun:
    
    @staticmethod
    def inst():
        return Singleton()


# if __name__ == "__main__":
#     a = Sun.inst()
#     b = Sun.inst()
#     print(a is b)
