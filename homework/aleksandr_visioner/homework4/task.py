import pprint
from typing import Any

my_dict: dict[str, Any] = {
    'tuple': ([1, 2], 3, 4, True, 'a'),  # Кортеж с 5 элементами
    'list': [{10, 20}, None, False, 'Text', (3, 4)],  # Список с 5 элементами
    'dict': {  # Словарь с 5 парами ключ-значение
        'one': (1, 2),
        'two': {3, 4},
        'three': [5, 6],
        'four': {'text_key': 'Text'},
        'five': 5
    },
    'set': {100.99, 'abc', True, (1,), None}  # Множество с 5 элементами
}

# 1) Действия с элементами словаря my_dict: tuple
print('Последний элемент кортежа: ' + my_dict['tuple'][-1])

# 2) Действия с элементами словаря my_dict: list
my_dict['list'].append('new_element')
my_dict['list'].pop(1)

# 3) Действия с элементами словаря my_dict: dict
# print('Последний элемент кортежа: ' + my_dict['dict'][-1])
my_dict['dict'][('i am a tuple',)] = 'new_value'
del my_dict['dict']['five']

# 4) Действия с элементами словаря my_dict: set
my_dict['set'].add(200)
my_dict['set'].remove(None)

# 5) Выводим весь словарь на экран
# print(my_dict)
print('Словать выглядит так:')
pprint.pprint(my_dict, indent=4, width=100)
