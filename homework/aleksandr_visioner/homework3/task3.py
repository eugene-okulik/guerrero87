# Даны два числа. Найти среднее арифметическое и среднее геометрическое этих чисел

a = float(input('Введите первое число (a): '))
b = float(input('Введите первое число (b): '))

arithmetic_avg_value = (a + b) / 2
geometric_avg_value = (a * b) ** 0.5

print('Среднее арифметическое двух чисел: ', arithmetic_avg_value)
print('Среднее геометрическое двух чисел: ', geometric_avg_value)
