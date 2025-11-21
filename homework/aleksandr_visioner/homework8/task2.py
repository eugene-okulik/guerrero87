import sys

sys.set_int_max_str_digits(21000)


def fibonacci_generator(start_a=0, start_b=1):
    a, b = start_a, start_b
    while True:
        yield a
        a, b = b, a + b


def get_fibonacci(n):
    if n < 0:
        raise ValueError("Номер должен быть > 0")

    fib_gen = fibonacci_generator()

    count = 0
    current_fib = None
    while count <= n:
        current_fib = next(fib_gen)
        count += 1

    return current_fib


print(f"5-е число Фибоначчи: {get_fibonacci(4)}")
print(f"200-е число Фибоначчи: {get_fibonacci(199)}")
print(f"1000-е число Фибоначчи: {get_fibonacci(999)}")
print(f"1000000-е число Фибоначчи: {get_fibonacci(100000)}")
