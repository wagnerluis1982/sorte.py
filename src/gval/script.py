# encoding=utf8
from __future__ import print_function

import getopt
import sys

from .loteria import Loteria, QuantidadeInvalida

def show_usage():
	print("Uso: %s LOTERIA" % sys.argv[0])
	print("""Gerador e Verificador de Apostas da Loteria\n
Informando somente a LOTERIA será gerada uma aposta

Argumentos:
  -q --quantidade   Quantas apostas deverão ser geradas. Padrão: 1
  -n --numeros      Quantos números cada aposta gerada terá. Se não informado
                      o padrão depende da LOTERIA informada
  -h --help         Mostra esta ajuda e finaliza""")

def error(*args, **kwargs):
    print(*args, file=sys.stderr)
    usage = kwargs.get('usage', True)
    if usage:
        show_usage()
    errcode = kwargs.get('code')
    if isinstance(errcode, int):
        sys.exit(errcode)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
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

    ori_nome, nome = args[0], args[0].lower()
    if nome not in ("quina",):
        error("loteria '%s' não suportada" % ori_nome, code=3)

    lote = Loteria(nome)
    print("Gerador de Apostas da", nome.title())
    try:
        aposta1 = lote.gerar_aposta(numeros)
    except QuantidadeInvalida, err:
        error("'%s'" % ori_nome, "não gera apostas com", err.valor, "números",
                usage=False, code=4)
    else:
        if quantidade == 1:
            print(' '.join("%02d" % n for n in aposta1))
        else:
            qdigitos = len(str(quantidade))
            print('#', '0'*(qdigitos-1), "1 = ",
                    ' '.join("%02d" % n for n in aposta1), sep='')
            for i in xrange(2, quantidade+1):
                aposta = lote.gerar_aposta(numeros)
                print('#', '0'*(qdigitos - len(str(i))), "%d = " % i,
                        ' '.join("%02d" % n for n in aposta), sep='')


if __name__ == "__main__":
    main()
