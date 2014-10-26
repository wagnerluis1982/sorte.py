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

Opções de consulta:
  -c --concurso     Número do concurso para consultar ou verificar

Opções gerais:
  -h --help         Mostra esta ajuda e finaliza

O valor de LOTERIA pode ser: """, ', '.join(sorted(loterica.LOTERIAS))])


def error(*args, **kwargs):
    print(*args, file=sys.stderr)
    if kwargs.get('show_help', True):
        print(help_msg)
    return kwargs.get('code', 255)


def exec_gerar(loteria, quantidade, numeros):
    try:
        aposta1 = loteria.gerar_aposta(numeros)
    except loterica.QuantidadeInvalida, err:
        return error("ERRO: não dá para gerar aposta da %s com %d números" %
                err.args, show_help=False, code=5)

    print("# gerador da", loteria.nome)
    print(' '.join("%02d" % n for n in aposta1))
    for i in xrange(2, quantidade+1):
        aposta = loteria.gerar_aposta(numeros)
        print(' '.join("%02d" % n for n in aposta))


def exec_consultar(loteria, concursos):
    consultados = set()
    for c in concursos:
        if c not in consultados:
            consultados.add(c)
            try:
                result = loteria.consultar(c)
            except loterica.LoteriaNaoSuportada, err:
                return error("ERRO: consulta para '%s' não implementada" %
                        err.args, show_help=False, code=6)
            except loterica.ResultadoNaoDisponivel, err:
                return error("ERRO: resultado da %s %d não disponível" %
                        err.args, show_help=False, code=6)

            print("# resultado da %s %d" % (loteria.nome, result['concurso']))
            print("numeros:")
            for res_nums in result['numeros']:
                print('-', ' '.join("%02d" % n for n in res_nums))


def __print_closure(stdout):
    def pf(*args, **kwargs):
        kwargs.setdefault('file', stdout)
        __builtin__.print(*args, **kwargs)
    return pf


def main(argv=sys.argv, stdout=sys.stdout, cfg_path=None):
    # Redefine 'print' para usar outra stdout passado como parâmetro
    global print
    print = __print_closure(stdout)

    try:
        opts, args = getopt.gnu_getopt(argv[1:],
        # opções curtas
        "hn:q:c:",
        # opções longas
        ["help", "numeros=", "quantidade=", "concurso="])
    except getopt.GetoptError, err:
        opt = (len(err.opt) == 1 and '-' or '--') + err.opt
        return error("ERRO: opção", opt, "desconhecida", code=1)

    # Avalia os parâmetros passados
    numeros = None
    quantidade = None
    concursos = []
    for option, arg in opts:
        if option in ("-h", "--help"):
            print(help_msg)
            return
        elif option in ("-n", "--numeros"):
            numeros = int(arg)
        elif option in ("-q", "--quantidade"):
            quantidade = int(arg)
        elif option in ("-c", "--concurso"):
            if arg.isdigit():
                concursos.append(int(arg))
            else:
                concursos.append(-1)

    if len(args) != 1:
        return error("ERRO: deve ser informado uma loteria", code=2)

    nome = args[0]
    try:
        loteria = loterica.Loteria(nome.lower(), cfg_path=cfg_path)
    except loterica.LoteriaNaoSuportada:
        return error("ERRO: loteria '%s' não suportada" % nome, code=3)

    if concursos:
        if quantidade or numeros:
            return error("ERRO: parâmetros incompatíveis", code=4)
        return exec_consultar(loteria, concursos)
    else:
        return exec_gerar(loteria, quantidade or 1, numeros)


if __name__ == "__main__":
    sys.exit(main())
