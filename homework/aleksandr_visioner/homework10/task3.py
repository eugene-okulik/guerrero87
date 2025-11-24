def operation_router(func):
    def wrapper(a, b, operation=None):
        if a < 0 or b < 0:
            op = '*'
        elif a == b:
            op = '+'
        elif a > b:
            op = '-'
        else:
            op = '/'
        return func(a, b, op)

    return wrapper


@operation_router
def calc(a, b, operation):
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else "Ошибка: деление на ноль"
    }
    print(f"Выполняется операция: {a} {operation} {b}")
    return operations.get(operation, lambda x, y: "Неизвестная операция")(a, b)


try:
    x, y = float(input("Первое число: ")), float(input("Второе число: "))
    print(f"Результат: {calc(x, y)}")
except ValueError:
    print("Ошибка ввода числа")
