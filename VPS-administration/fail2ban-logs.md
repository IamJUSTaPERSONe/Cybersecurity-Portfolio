
# Анализ работы fail2ban на VPS

## Конфигурация
- Сервер: VPS (Нидерланды)
- ОС: Ubuntu 22.04/24.04
- Защита: fail2ban для SSH (порт 22)

## Статистика (на 2026-04-04)

| Параметр | Значение |
|----------|----------|
| Всего неудачных попыток входа | 35 784 |
| Всего заблокированных IP | 5 082 |
| Сейчас заблокировано | 7 |
| Текущие failed попытки | 1 |


## Выводы
- Сервер активно атакуется (35k+ попыток брутфорса)
- fail2ban успешно блокирует ~14% от всех попыток (5k+ IP)
- Блокировка работает автоматически, без участия администратора

## Скриншоты
- <img width="862" height="225" alt="image" src="https://github.com/user-attachments/assets/0e886ed7-b6ff-4395-8e7a-b71cc56d73c4" />
- <img width="939" height="59" alt="image" src="https://github.com/user-attachments/assets/ba55f1f8-03bb-4d81-89dc-a0fd6125f83c" />

## Команды для проверки (для воспроизведения)
```bash
sudo fail2ban-client status sshd
sudo fail2ban-client banned
