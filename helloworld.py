#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import time
from datetime import datetime
import sys

HOST = "0.0.0.0"  # o "127.0.0.1" si sólo quieres acceso local
PORT = 8080

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Hello World"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # Opcional: silenciar logging por cada petición (evita muchas líneas en consola)
    def log_message(self, format, *args):
        return

def run_server():
    try:
        server = ThreadingHTTPServer((HOST, PORT), HelloHandler)
    except OSError as e:
        print(f"ERROR al iniciar el servidor en {HOST}:{PORT} -> {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Servidor HTTP iniciado en http://{HOST}:{PORT} (press Ctrl+C to stop)")
    try:
        server.serve_forever()
    finally:
        server.server_close()

if __name__ == "__main__":
    # Lanzar servidor en hilo daemon (no bloqueará el main loop que imprime la hora)
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Bucle principal: imprime la hora cada minuto (y responde a Ctrl+C para cerrar)
    try:
        while True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Dormir 10 segundos (si quieres precisión a minuto exacto, ver nota abajo)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario. Saliendo...")
        # server_thread es daemon: el proceso terminará; si quieres un cierre más limpio,
        # podrías no poner daemon=True y llamar a server.shutdown() desde aquí.
        sys.exit(0)
