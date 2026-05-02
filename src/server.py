from http.server import BaseHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Для определения Content-Type
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
}

routes = {
    "/": "index.html",
    "/categories": "categories.html",
    "/category/1": "category_1.html",
    "/contacts": "contacts.html",
}


class MyServer(BaseHTTPRequestHandler):
    """Специальный класс, который отвечает за обработку входящих запросов от клиентов."""

    def do_GET(self):
        """Метод для обработки входящих GET-запросов."""
        try:
            if self.path.startswith("/static/"):
                self.serve_static()
            else:
                template_name = routes.get(self.path, "templates/404.html")
                self.serve_html(template_name)

        except FileNotFoundError:
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

    def serve_static(self):
        """Отдаёт статический файл из папки static"""
        file_path = BASE_DIR / self.path.lstrip("/")
        if not file_path.exists() or not file_path.is_file():
            self.send_error(404, "File not found")
            return

        # Определяем Content-Type по расширению
        suffix = file_path.suffix.lower()
        content_type = CONTENT_TYPES.get(suffix, "application/octet-stream")

        # Читаем файл как бинарный (картинки, шрифты и т.п.)
        with open(file_path, "rb") as f:
            data = f.read()

        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
