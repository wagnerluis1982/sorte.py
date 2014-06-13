# encoding=utf8
from __future__ import print_function

import __builtin__
import getopt
import sys

from . import loterica

help_msg = ''.join([
"Uso: %s LOTERIA [opcoes]\n" % sys.argv[0],
"""
O `sorte.py` é um gerador e verificador de apostas de loterias
Sem opções explícitas é gerada uma aposta da LOTERIA informada

Opções de geração de apostas:
  -q --quantidade   Quantas apostas deverão ser geradas. Padrão: 1
  -n --numeros      Quantos números para marcar em cada aposta gerada. Se não
                      informado o padrão depende da LOTERIA informada

Opções gerais:
  -h --help         Mostra esta ajuda e finaliza

""",
"O valor de LOTERIA pode ser: ", ', '.join(sorted(loterica.LOTERIAS))])

def error(*args, **kwargs):
    print(*args, file=sys.stderr)
    if kwargs.get('show_help', True):
        print(help_msg)
    return kwargs.get('code', 255)

def exec_gerador(loteria, quantidade, numeros):
    print("Gerador de Apostas da", loteria.nome)
    try:
        aposta1 = loteria.gerar_aposta(numeros)
    except loterica.QuantidadeInvalida, err:
        return error("não dá para gerar aposta da %s com %d números" %
                (loteria.nome, err.valor), show_help=False, code=4)

    if quantidade == 1:
        print(' '.join("%02d" % n for n in aposta1))
    else:
        qdigitos = len(str(quantidade))
        print('#', '0'*(qdigitos-1), "1 = ",
                ' '.join("%02d" % n for n in aposta1), sep='')
        for i in xrange(2, quantidade+1):
            aposta = loteria.gerar_aposta(numeros)
            print('#', '0'*(qdigitos - len(str(i))), "%d = " % i,
                    ' '.join("%02d" % n for n in aposta), sep='')

def main(argv=sys.argv, stdout=sys.stdout):
    # Redefine 'print' para usar outra stdout passado como parâmetro
    global print
    def print(*args, **kwargs):
        kwargs.setdefault('file', stdout)
        __builtin__.print(*args, **kwargs)

    try:
        opts, args = getopt.gnu_getopt(argv[1:],
        # opções curtas
        "hn:q:",
        # opções longas
        ["help", "numeros=", "quantidade="])
    except getopt.GetoptError, err:
        opt = (len(err.opt) == 1 and '-' or '--') + err.opt
        return error("opção", opt, "desconhecida", code=1)

    # Avalia os parâmetros passados
    numeros = None
    quantidade = None
    for option, arg in opts:
        if option in ("-h", "--help"):
            print(help_msg)
            return
        elif option in ("-n", "--numeros"):
            numeros = int(arg)
        elif option in ("-q", "--quantidade"):
            quantidade = int(arg)

    if len(args) != 1:
        return error("deve ser informado uma loteria", code=2)

    nome = args[0]
    try:
        loteria = loterica.Loteria(nome.lower())
    except loterica.LoteriaNaoSuportada:
        return error("loteria '%s' não suportada" % nome, code=3)

    return exec_gerador(loteria, quantidade or 1, numeros)


if __name__ == "__main__":
    sys.exit(main())
