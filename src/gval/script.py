# encoding=utf8
from __future__ import print_function

import getopt
import sys

from .loteria import Loteria

def usage():
	print("Uso: %s LOTERIA" % sys.argv[0])
	print("""Gerador e Verificador de Apostas da Loteria\n
Informando somente a LOTERIA será gerada uma aposta

Argumentos:
  -q --quantidade   Quantas apostas deverão ser geradas. Padrão: 1
  -n --numeros      Quantos números cada aposta gerada terá. Se não informado
                      o padrão depende da LOTERIA informada
  -h --help         Mostra esta ajuda e finaliza""")

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
        # opções curtas
        "hn:q:",
        # opções longas
        ["help", "numeros=", "quantidade="])
    except getopt.GetoptError, err:
        opt = (len(err.opt) == 1 and '-' or '--') + err.opt
        print("opção", opt, "desconhecida")
        usage()
        sys.exit(1)

    numeros = None
    quantidade = 1
    for option, arg in opts:
        if option in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-n", "--numeros"):
            numeros = int(arg)
        elif option in ("-q", "--quantidade"):
            quantidade = int(arg)

    if len(args) == 0:
        usage()
        sys.exit(0)
    if len(args) > 1:
        print("deve ser informado apenas uma loteria")
        usage()
        sys.exit(3)

    nome = args[0]
    if nome.lower() not in ("quina",):
        print("loteria '%s' não suportada" % nome)
        usage()
        sys.exit(3)

    lote = Loteria(nome)
    print("Geração de Aposta da", nome.title())
    if quantidade == 1:
        print(' '.join("%02d" % n for n in lote.gerar_aposta(numeros)))
    else:
        qdigitos = len(str(quantidade))
        for i in xrange(1, quantidade+1):
            print('#', '0'*(qdigitos - len(str(i))), "%d = " % i,
                    ' '.join("%02d" % n for n in lote.gerar_aposta(numeros)),
                    sep='')


if __name__ == "__main__":
    main()
