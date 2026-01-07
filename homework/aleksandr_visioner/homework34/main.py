import time
from datetime import datetime
import requests

while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Текущее время: {current_time}")
    
    try:
        response = requests.get("https://google.com")
        print(f"Статус запроса к Google: {response.status_code}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    time.sleep(2)