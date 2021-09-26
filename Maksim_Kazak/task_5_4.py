a = "I am global variable!"


def enclosing_function():
    a = "I am variable from enclosed function!"

    def inner_function():

        a = "I am local variable!"
        print(a)

    return inner_function()


def enclosing_function_global_a():
    a = "I am variable from enclosed function!"

    def inner_function():
        global a
        print(a)

    return inner_function()


def enclosing_function_enclosed_a():
    a = "I am variable from enclosed function!"

    def inner_function():
        nonlocal a
        print(a)

    return inner_function()
