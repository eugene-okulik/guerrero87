import datetime

file_path = '../../eugene_okulik/hw_13/data.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        left_part = line.strip().split(' - ')[0]
        number, date_str = left_part.split('. ', 1)
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')

        if number == '1':
            print((dt + datetime.timedelta(days=7)).strftime('%Y-%m-%d '
                                                             '%H:%M:%S.%f'))
        elif number == '2':
            days = ["понедельник", "вторник", "среда", "четверг", "пятница",
                    "суббота", "воскресенье"]
            print(days[dt.weekday()])
        elif number == '3':
            now = datetime.datetime.now()
            delta = now - dt
            print(f"{delta.days} дней назад")
