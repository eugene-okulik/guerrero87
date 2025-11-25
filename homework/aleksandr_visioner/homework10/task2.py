def repeat_me(func):
    def wrapper(*args, **kwargs):
        count = kwargs.pop('count', 1)
        result = None
        for i in range(count):
            result = func(*args, **kwargs)
        return result

    return wrapper


@repeat_me
def example(text):
    print(text)


@repeat_me
def add_sum(a, b, **kwargs):
    result = a + b
    print(f"Сумма: {result}")
    return result


# Запуск примеров:
print("--- example('print me', count=2) ---")
example('print me', count=2)

print("\n--- example('print me without count') ---")
example('print me without count')

print("\n--- add_sum(1, 2, count=3) ---")
print(f"Результат: {add_sum(1, 2, count=3)}")
