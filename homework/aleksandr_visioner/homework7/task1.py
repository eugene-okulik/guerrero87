import random


def play_game_once():
    random_number = random.randint(0, 10)
    print("Попробуйте угадать цифру от 0 до 10")
    user_input = None
    while user_input != random_number:
        try:
            user_input = int(input("Введите вашу цифру: "))
            if int(user_input) > 10:
                print("Вы ввели число > 10. Введите от 0 до 10.")
            elif int(user_input) < 0:
                print("Вы ввели число < 0. Введите от 0 до 10.")
            elif user_input != random_number:
                print("Не угадали! Попробуйте снова.")
            else:
                print(f"Поздравляю! Вы угадали число {random_number}.")
        except ValueError:
            print("Ошибка ввода. Пожалуйста, введите целую цифру.")


def main_game_loop():
    play_again_choice = "y"
    while play_again_choice.lower() == "y":
        play_game_once()
        play_again_choice = input(
            "Хотите сыграть еще раз? Введите 'y' для продолжения: ")
    print("Спасибо за игру! До свидания.")


main_game_loop()
