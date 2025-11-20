temperatures = [20, 15, 32, 34, 21, 19, 25, 27, 30, 32,
                34, 30, 29, 25, 27, 22, 22, 23, 25, 29,
                29, 31, 33, 31, 30, 32, 30, 28, 24, 23]

hot_days_list = list(filter(lambda temp: temp > 28, temperatures))

print(f"Список всех жарких дней (выше 28°C): {hot_days_list}")
print(f"Самая высокая температура среди жарких дней: {max(hot_days_list)}°C")
print(f"Самая низкая температура среди жарких дней: {min(hot_days_list)}°C")
print(f"Средняя температура среди жарких дней: "
      f"{round(sum(hot_days_list) / len(hot_days_list),2)}°C")
