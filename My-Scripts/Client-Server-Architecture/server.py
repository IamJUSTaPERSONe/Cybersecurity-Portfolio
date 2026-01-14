import os
import socket
import time

# Создаем сокет (типо как телефон для общения)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# На каком адресе и порту будет работать сервер
server_address = ('', 12345)
server_socket.bind(server_address)

try:
    # Сервер слушает максимально 1 подключение
    server_socket.listen(1)
    print("Сервер запущен и ждет подключения")
except Exception as e:
    print(f"Неизвестная ошибка в ходе запуска сервера: {e}")

# Принимает подключение от клиента
client_socket, client_address = server_socket.accept()
print(f"{client_address} - подключен к серверу")

# Получаем файл. 100 - это первые 100 байт, в которых клиент отправит длину имени и имя
data = client_socket.recv(100)
if not data:
    print("Клиент не передал данные")
    client_socket.close()
    server_socket.close()
    exit()

# Узнаем длину имени файла и преобразуем в число
filename_lght = int(data[:4].decode('utf-8'))

# Зная длину получаем имя файла
filename = data[4:4 + filename_lght].decode('utf-8')

# Тут определяем новое имя для полученного файла, сохраняя его исходное
safe_filename = os.path.basename(filename)

timestamp = int(time.time())
file_counter = 1

base_name, ext = os.path.splitext(safe_filename)
new_filename = f'{base_name}_{timestamp}{ext}'
filepath = os.path.join(new_filename)

print(f"Файл {filename} сохранен как {new_filename}")

# Открываем файл для записи в бинарном режиме
with open (new_filename, 'wb') as f:
    while True:
        # Получаем кусок данных размером от 1024 байт
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        f.write(chunk)

print(f"Путь: {os.path.abspath(filepath)}")

client_socket.sendall("Сервер получил данные".encode('utf-8'))

client_socket.close()
server_socket.close()
print("Сервер закрыл доступ")

