"""Проверяет доступность сайта"""
import requests
import time


def check_website(url):

    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            return f"{url} - доступен. Время ответа {elapsed_time:.2f}"
        else:
            return f"{url} - не доступен. код ошибки: {response.status_code}"

    except requests.exceptions.Timeout as tm:
        return "Превышен лимит ожидания", tm
    except Exception as e:
        return " Неизвестная ошибка", e

sites = ['http://testphp.vulnweb.com', 'https://testphp.vulnweb.com', 'https://github.com']
for site in sites:
    print(check_website(site))
