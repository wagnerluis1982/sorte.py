import atexit
import http.server
import multiprocessing
import os


# declaração de globais
global server_url


def start_server():
    if not getattr(start_server, "status", 0):
        # inicia servidor
        server = FixtureHttpServer()
        server.start()
        atexit.register(server.terminate)
        # guarda a porta e cria URL
        global server_url
        server_url = "http://127.0.0.1:%d" % server.port
        # marca servidor como já inicializado
        start_server.status = 1


class FixtureRequestHandler(http.server.CGIHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        # Desabilitando mensagens de log no terminal.
        pass

    def guess_type(self, path):
        # Se nome do arquivo indica um charset retorna 'text/html' e charset
        for charset in ("ascii", "iso-8859-1", "utf-8"):
            if charset in path:
                return "text/html; charset=%s" % charset
        # Se não achou um charset retorna mimetype default
        return super().guess_type(path)


class FixtureHttpServer(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self.httpd = http.server.HTTPServer(("127.0.0.1", 0), FixtureRequestHandler)
        self.port = self.httpd.server_port

    def run(self):
        fixtures_dir = os.path.join(os.path.dirname(__file__))
        os.chdir(fixtures_dir)
        self.httpd.serve_forever()
