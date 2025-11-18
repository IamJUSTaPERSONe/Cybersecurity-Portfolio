from flask import Flask, request, render_template_string
import datetime
import json

app = Flask(__name__)

# Хранилище данных
collected_data = []

# Код страницы в браузере
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Опрос</title>
</head>
<body onload="collectInfo()">
    <h1>Примите участие в опросе!</h1>

    <form action="/submit" method="post">
        <input type="text" name="name" placeholder="Имя" required><br><br>
        <input type="email" name="email" placeholder="Email" required><br><br>
        <button type="submit">Участвовать</button>
    </form>

    <script>
        function collectInfo() {
            // Собираем данные сразу при загрузке страницы
            const info = {
                screen: screen.width + "x" + screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                languages: navigator.languages,
                platform: navigator.platform,
                cookies: navigator.cookieEnabled,
                timestamp: new Date().toISOString()
            };

            // Отправляем на сервер
            fetch('/track', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(info)
            });
        }

        // Собираем движения мыши
        let moves = [];
        document.addEventListener('mousemove', (e) => {
            moves.push({x: e.clientX, y: e.clientY, t: Date.now()});
            if (moves.length > 10) {
                fetch('/track-mouse', {
                    method: 'POST', 
                    body: JSON.stringify({movements: moves})
                });
                moves = [];
            }
        });
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    # Собираем базовые данные из заголовков
    base_info = {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'referer': request.headers.get('Referer'),
        'visit_time': datetime.datetime.now().isoformat(),
        'method': 'initial_visit'
    }
    collected_data.append(base_info)

    return render_template_string(HTML_TEMPLATE)


@app.route('/track', methods=['POST'])
def track():
    # Получаем данные из JavaScript
    js_data = request.get_json()
    js_data['ip'] = request.remote_addr
    js_data['method'] = 'javascript_tracking'
    collected_data.append(js_data)

    print("📱 Собраны JS-данные:", js_data)
    return 'OK'


@app.route('/track-mouse', methods=['POST'])
def track_mouse():
    mouse_data = request.get_json()
    mouse_data['ip'] = request.remote_addr
    mouse_data['method'] = 'mouse_tracking'
    collected_data.append(mouse_data)

    print("🖱️ Движения мыши:", len(mouse_data.get('movements', [])))
    return 'OK'


@app.route('/submit', methods=['POST'])
def submit():
    form_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'ip': request.remote_addr,
        'submit_time': datetime.datetime.now().isoformat(),
        'method': 'form_submission'
    }
    collected_data.append(form_data)

    return f'''
    <h2>Спасибо, {request.form['name']}!</h2>
    <p>Ваши данные получены.</p>
    '''


@app.route('/stats')
def stats():
    stats_html = "<h1>📊 Вся собранная информация</h1>"

    for i, data in enumerate(collected_data, 1):
        stats_html += f"<div style='border:1px solid #000; margin:10px; padding:10px;'>"
        stats_html += f"<h3>Запись #{i} - {data.get('method', 'unknown')}</h3>"
        stats_html += f"<pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>"
        stats_html += "</div>"

    return stats_html


if __name__ == '__main__':
    print('Запуск приложения')
    '''Для тестирования приложения с другого устройства в локальной сети - использовать IP хоста
    '''
    app.run(host='127.0.0.1', port=5000, debug=False)