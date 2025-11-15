# Даны числа x и y. Получить x − y / 1 + xy

x = float(input('Введите первое число (x): '))
y = float(input('Введите второе число (y): '))

result = (x - y) / (1 + x * y)

print('Результат: ', result)
