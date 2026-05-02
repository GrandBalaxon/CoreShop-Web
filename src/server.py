from http.server import BaseHTTPRequestHandler
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

class MyServer(BaseHTTPRequestHandler):
    """Специальный класс, который отвечает за обработку входящих запросов от клиентов."""

    def do_GET(self):
        """Метод для обработки входящих GET-запросов."""
        if self.path == "/" or self.path == "/index.html":
            self.serve_html("index.html")
        elif self.path == "/contacts":
            self.serve_html("contacts.html")
        else:
            self.send_error(404, "Page not found")

    def serve_html(self, template_name):
        """Отдаёт HTML-шаблон из папки templates"""
        template_path = BASE_DIR / "templates" / template_name

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                html = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        except FileNotFoundError:
            self.send_error(404, "Page not found")
