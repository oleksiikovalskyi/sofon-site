#!/usr/bin/env python3
"""Статичний dev-сервер для сайту Sofon, який забороняє браузеру кешувати.

Навіщо: звичайний `python -m http.server` віддає Last-Modified, і браузер
тримає CSS/JS/HTML у кеші. Через це правки не видно доти, доки не зробиш
жорстке перезавантаження — легко подумати, що зміни не застосувалися.
Тут кожна відповідь іде з no-store, тож у браузері завжди свіжа версія.

Запуск:  py .claude/serve.py [порт]   (типово 8123, з кореня репозиторію)
"""
import http.server
import socketserver
import sys


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):  # тихіше в консолі
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", port), NoCacheHandler) as httpd:
        print("serving http://localhost:%d (no-cache)" % port)
        httpd.serve_forever()
