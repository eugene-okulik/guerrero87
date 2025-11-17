text1 = 'результат операции: 42'
text2 = 'результат операции: 514'
text3 = 'результат работы программы: 9'

print(f"Результат text1 строки: {int(text1[text1.index(':') + 1:]) + 10}")
print(f"Результат text2 строки: {int(text2[text2.index(':') + 1:]) + 10}")
print(f"Результат text3 строки: {int(text3[text3.index(':') + 1:]) + 10}")
