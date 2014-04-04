# encoding=utf8
from __future__ import print_function

import __builtin__
import getopt
import sys

from . import loteria

def show_usage():
	print("Uso: %s LOTERIA" % sys.argv[0])
	print("""Gerador e Verificador de Apostas da Loteria\n
Informando somente a LOTERIA será gerada uma aposta

Argumentos:
  -q --quantidade   Quantas apostas deverão ser geradas. Padrão: 1
  -n --numeros      Quantos números cada aposta gerada terá. Se não informado
                      o padrão depende da LOTERIA informada
  -h --help         Mostra esta ajuda e finaliza

O valor de LOTERIA pode ser:""", ', '.join(loteria.LOTERIAS))

def error(*args, **kwargs):
    print = kwargs.get('print_function', __builtin__.print)
    print(*args, file=sys.stderr)
    usage = kwargs.get('usage', True)
    if usage:
        show_usage()
    errcode = kwargs.get('code')
    if isinstance(errcode, int):
        sys.exit(errcode)

def exec_gerador(instancia, quantidade, numeros, print_function=print):
    print = print_function
    print("Gerador de Apostas da", instancia.nome)
    try:
        aposta1 = instancia.gerar_aposta(numeros)
    except loteria.QuantidadeInvalida, err:
        error("não dá para gerar aposta da %s com %d números" %
                (instancia.nome, err.valor), usage=False, code=4)

    if quantidade == 1:
        print(' '.join("%02d" % n for n in aposta1))
    else:
        qdigitos = len(str(quantidade))
        print('#', '0'*(qdigitos-1), "1 = ",
                ' '.join("%02d" % n for n in aposta1), sep='')
        for i in xrange(2, quantidade+1):
            aposta = instancia.gerar_aposta(numeros)
            print('#', '0'*(qdigitos - len(str(i))), "%d = " % i,
                    ' '.join("%02d" % n for n in aposta), sep='')

def main(argv=sys.argv, stdout=sys.stdout):
    def print(*args, **kwargs):
        __builtin__.print(*args, file=stdout, **kwargs)

    try:
        opts, args = getopt.gnu_getopt(argv[1:],
        # opções curtas
        "hn:q:",
        # opções longas
        ["help", "numeros=", "quantidade="])
    except getopt.GetoptError, err:
        opt = (len(err.opt) == 1 and '-' or '--') + err.opt
        error("opção", opt, "desconhecida", code=1)

    numeros = None
    quantidade = 1
    for option, arg in opts:
        if option in ("-h", "--help"):
            show_usage()
            sys.exit(0)
        elif option in ("-n", "--numeros"):
            numeros = int(arg)
        elif option in ("-q", "--quantidade"):
            quantidade = int(arg)

    if len(args) == 0:
        show_usage()
        sys.exit(0)
    if len(args) > 1:
        error("deve ser informado apenas uma loteria", code=2)

    nome = args[0]
    try:
        instancia = loteria.Loteria(nome.lower())
    except loteria.LoteriaNaoSuportada:
        error("loteria '%s' não suportada" % nome, code=3)

    exec_gerador(instancia, quantidade, numeros, print_function=print)


if __name__ == "__main__":
    main()
