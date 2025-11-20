import random

bonus = random.choice([True, False])
while True:
    try:
        user_input = input("Введите вашу базовую зарплату: ")
        salary = int(user_input)
        if salary < 0:
            print("Зарплата не может быть отрицательной. Попробуйте снова.")
            continue
        break
    except ValueError:
        print("Ошибка ввода. Пожалуйста, введите положительную сумму.")

if bonus:
    print(f"{salary}, {bonus} - "
          f"${salary + random.randint(int(salary * 0.1), int(salary * 0.5))}")
else:
    print(f"{salary}, {bonus} - ${salary}")
