#!/usr/bin/env python3
import cgi
import os
import socket

# obtém parâmetros do usuário
fields = cgi.FieldStorage()
nome = fields.getvalue('nome')
concurso = fields.getvalue('concurso')

# abre arquivo de resultado
caminho = os.path.join('resultados', '%s-%s.htm' % (nome, concurso))
f = open(caminho, 'rb')

# envia tipo
print("Content-Type: text/html; charset=ISO-8859-1")

# fim dos cabeçalhos
print(end='\r\n', flush=True)

# operação (possivelmente) zero-copy para enviar resultado
# @see: https://docs.python.org/dev/library/socket.html#socket.socket.sendfile
sock = socket.socket(fileno=1)
sock.sendfile(f)
