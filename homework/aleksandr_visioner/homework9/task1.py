from datetime import datetime

date_string = "Jan 15, 2023 - 12:05:33"
python_date = datetime.strptime(date_string, "%b %d, %Y - %H:%M:%S")

print(f"1) Дата в питоновском формате: {python_date}")
print(f"2) Полное название месяца: {python_date.strftime('%B')}")
print(f"3) Отформатированная дата и время: "
      f"{python_date.strftime('%d.%m.%Y, %H:%M')}")
