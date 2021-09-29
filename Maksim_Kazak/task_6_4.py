class Bird:

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"{self.name} bird can walk and fly"

    def fly(self):
        print(f"{self.name} bird can fly")

    def walk(self):
        print(f"{self.name} bird can walk")


class FlyingBird(Bird):

    def __init__(self, name: str, ration: str = "grains"):
        super().__init__(name)
        self.ration = ration

    def eat(self):
        print(f"{self.name} eats mostly {self.ration}")


class NonFlyingBird(Bird):

    def __init__(self, name: str, ration: str = "fish"):
        super().__init__(name)
        self.ration = ration

    def __str__(self):
        return f"{self.name} bird can walk and swim"

    def fly(self):
        raise AttributeError(f"{self.name} object has no attribute 'fly'")

    def swim(self):
        print(f"{self.name} bird can swim")

    def eat(self):
        print(f"{self.name} eats mostly {self.ration}")


class SuperBird(FlyingBird, NonFlyingBird):

    def __init__(self, name: str, ration: str = "fish"):
        super().__init__(name, ration)

    def __str__(self):
        return f"{self.name} can walk, swim and fly"

    def fly(self):
        return FlyingBird.fly(self)


# if __name__ == "__main__":
    # b = Bird("Any")
    # b.walk()
    # p = NonFlyingBird("Penguin", "fish")
    # p.swim()
    # p.fly()
    # p.eat()
    # c = FlyingBird("Canary")
    # print(c)
    # c.eat()
    # s = SuperBird("Gull")
    # print(s)
    # s.eat()
    # print(SuperBird.__mro__)
