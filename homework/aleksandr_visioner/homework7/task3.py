text1 = 'результат операции: 42'
text2 = 'результат операции: 514'
text3 = 'результат работы программы: 209'
text4 = 'результат: 2'

my_strings = [text1, text2, text3, text4]


def result_operation(input_list):
    for i, s in enumerate(input_list):
        print(f"Результат text{i + 1} "
              f"строки: {int(s[s.index(':') + 1:]) + 10}")


result_operation(my_strings)
