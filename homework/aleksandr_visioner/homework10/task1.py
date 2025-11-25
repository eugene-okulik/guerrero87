def finish_me(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("finished")
        return result

    return wrapper


@finish_me
def example(text):
    print(text)


@finish_me
def add(a, b):
    print(f"Сумма {a} и {b} равна {a + b}")
    return a + b


print("Результат вызова example:")
example('print me')
add(1, 2)
