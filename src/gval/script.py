# encoding=utf8

import getopt
import sys

from .loteria import Loteria

def usage():
	print "Uso: %s LOTERIA" % sys.argv[0]
	print("Gerador e Verificador de Apostas da Loteria\n\n"
    "Informando somente a LOTERIA, é gerada uma aposta\n\n"
	"Argumentos:\n"
	"  -h --help         mostra esta ajuda e finaliza")

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
        # opções curtas
        "h",
        # opções longas
        ["help"])
    except getopt.GetoptError, err:
        opt = (len(err.opt) == 1 and '-' or '--') + err.opt
        print "opção", opt, "desconhecida"
        usage()
        sys.exit(1)

    for option, arg in opts:
        if option in ("-h", "--help"):
            usage()
            sys.exit(0)

    if len(args) != 1:
        print "deve ser informado um nome de loteria"
        usage()
        sys.exit(2)

    nome = args[0]
    if nome.lower() not in ("quina",):
        print "loteria '%s' não suportada" % nome
        usage()
        sys.exit(3)

    lote = Loteria(nome)
    print "Geração da", nome.title()
    print "- Aposta:", ' '.join("%02d" % n for n in lote.gerar_aposta())


if __name__ == "__main__":
    main()
