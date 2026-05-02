from http.server import BaseHTTPRequestHandler
from pathlib import Path


class MyServer(BaseHTTPRequestHandler):
    """Специальный класс, который отвечает за обработку входящих запросов от клиентов."""

    def do_GET(self):
        """Метод для обработки входящих GET-запросов."""
        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "text/html")  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа

        project_root = Path(__file__).parent.parent
        template_path = project_root / "templates" / "index.html"

        with open(template_path, "r", encoding="utf-8") as file:
            html = file.read()

        self.wfile.write(html.encode("utf-8"))
