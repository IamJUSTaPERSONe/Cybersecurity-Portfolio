# Некоторые из используемых команд

1. Установка сервера (в настройках виртуальной машины выбрать NAT для выхода в интернет для установки библиотек, далее сменить на сетевой мост)
```
sudo apt update
sudo apt install fly-admin-openvpn-server astra-openvpn-server
```
2. Проверка статуса сервера
```
sudo netstat -tulpn | grep 1194

# Проверяем интерфейс VPN 
ip a show tun0
```
3. Создать общую папку на виртуальной машине (сначала настроить общую папку в VirtualBox)
```
# Создаем точку монтирования
sudo mkdir -p /media/your_name
# Монтируем общую папку
sudo mount -t vboxsf your_name /media/your_name
# Проверяем, что она смонтировалась
ls /media/your_name
# Копируем в нее файлы из папке, где у нас лежит файл с ключем, конфигурацией и тп
sudo cp /etc/openvpn/keys/* /media/your_name/
# Даем права на чтение 
sudo chmod 644 /media/your_name/*
```
4. Перезагрузка
```
sudo reboot
```
5. Проверка какие файлы лежат в директории по указанному пути
```
ls -la /directory/
```
6. Редактировать файл с настройками сети (ctrl+o -> записать, enter -> пропустить изменение имени файла, ctrl+x -> выйти из редактирования)
```
sudo nano /etc/network/interfaces
```
7. Проверка статуса сервиса (если используется systemd)
```
sudo systemctl status openvpn-server@server
```
8. Просмотр логов в реальном времени (самое полезное при отладке!)
```
sudo journalctl -u openvpn-server@server -f
```
9. Проверка, запущен ли процесс OpenVPN
```
ps aux | grep openvpn
```

