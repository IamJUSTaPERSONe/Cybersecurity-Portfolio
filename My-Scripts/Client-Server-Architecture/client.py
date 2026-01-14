import os
import socket

# Создаем сокет клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Задаем адрес сервера
server_address = ('localhost', 12345)

try:
    client_socket.connect(server_address)
    print("Клиент успешно подключен к серверу", server_address)
except ConnectionRefusedError:
    print("Ошибка подключения к серверу")

filename = 'doc1.txt'

if not os.path.exists(filename):
    print("Файл не найден")
    client_socket.close()
    exit()

# Формируем инфу о файле
# Строка с именем файла
filename_bytes = filename.encode('utf-8')
# Длина файла
filename_len = len(filename_bytes)
# Делаем длину строкой и добавляем в начало четыре 0 (0008)
filename_len_str = str(filename_len).zfill(4)
# Создаем заголовок для отправки на сервер
header = filename_len_str.encode('utf-8') + filename_bytes

client_socket.sendall(header)
print("Идет передача файла")

# Отправляем файл
with open(filename, 'rb') as f:
    while True:
        chunk = f.read(1024)
        if not chunk:
            break
        # Отправляет файл по кускам
        client_socket.sendall(chunk)

# Закрываем отправку данных на сервер
client_socket.shutdown(socket.SHUT_WR)
print("Файл успешно доставлен")

# Получаем ответ от сервера
server_conf = client_socket.recv(1024)
print(f"Получен ответ сервера: '{server_conf.decode('utf-8')}'")

# Конец связи
client_socket.close()
print("Клиент отключен")