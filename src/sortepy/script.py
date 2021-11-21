import getopt
import re
import sys

from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple

from sortepy import loterica


help_msg = "".join(
    [
        "Uso: %s LOTERIA [opcoes] [APOSTA...]\n" % sys.argv[0],
        """
O `sorte.py` é um gerador e verificador de apostas de loterias
Sem opções explícitas é gerada uma aposta da LOTERIA informada

Opções de geração de apostas:
  -q --quantidade   Quantas apostas deverão ser geradas. Padrão: 1
  -n --numeros      Quantos números para marcar em cada aposta gerada. Se não
                      informado o padrão depende da LOTERIA informada

Opções de consulta ou conferência:
  -c --concurso     Número do concurso para consultar ou conferir. Pode ser
                      passada várias vezes
  -i --stdin        Recebe as apostas da entrada padrão, útil para manter as
                      apostas em um arquivo

  Se houver pelo menos uma aposta como argumento ou a opção -i for passada, o
    script assume a função de conferência de apostas

Opções gerais:
  -h --help         Mostra esta ajuda e finaliza

O valor de LOTERIA pode ser: """,
        ", ".join(sorted(loterica.LOTERIAS)),
    ]
)


def error(*args: Any, show_help: bool = True, code: int = 255, **kwargs: Any) -> int:
    print(*args, **kwargs)
    if show_help:
        print(help_msg)
    return code


def exec_gerar(loteria: loterica.Loteria, quantidade: int, numeros: int) -> int:
    """Executa a geração de números para apostas

    Parameters
    ----------
    loteria : Loteria
        Identifica a loteria usada para a geração de números
    quantidade : int
        O total de apostas para gerar
    numeros : int
        O total de números gerados em cada aposta

    Returns
    -------
    int
        Código de erro
    """
    if loteria.kind == loterica.K_TICKET:
        return error(
            "ERRO: loteria %s não gera apostas porque é tipo ticket" % loteria.nome,
            show_help=False,
            code=5,
        )
    try:
        for i in range(1, quantidade + 1):
            aposta = loteria.gerar_aposta(numeros)
            if i == 1:
                print("# gerador da", loteria.nome)
            print(" ".join("%02d" % n for n in aposta))
    except loterica.QuantidadeInvalida as err:
        return error(
            "ERRO: não dá para gerar aposta da %s com %d números" % err.args,
            show_help=False,
            code=5,
        )


def iter_resultados(
    fun: Callable[..., Dict[str, Any]], args: Tuple[List[int], ...], erros: Set[int]
) -> Iterable[Dict[str, Any]]:
    consultados = set()

    concursos = args[0]
    args = args[1:]
    while True:
        try:
            c = concursos.pop(0)
        except IndexError:
            return

        if c not in consultados:
            consultados.add(c)
            try:
                yield fun(c, *args)
            except loterica.ResultadoNaoDisponivel:
                erros.add(c)
                for i in reversed(range(len(concursos))):
                    if concursos[i] > c:
                        erros.add(concursos.pop(i))
                continue


def exec_consultar(loteria: loterica.Loteria, concursos: List[int]) -> int:
    erros = set()
    try:
        resultados = iter_resultados(loteria.consultar, (concursos,), erros)
    except loterica.LoteriaNaoSuportada as err:
        return error(
            "ERRO: consulta para '%s' não implementada" % err.args,
            show_help=False,
            code=6,
        )

    print("# resultados da", loteria.nome)
    print("%s:" % loteria.nome)

    for result in resultados:
        _numeros = result.get("numeros", ())

        # esse resultado não cria a chave 'numeros'
        if not _numeros:
            print("  -")
            print("   concurso: %d" % result["concurso"])
            print("   premios:")

            premios = result["premios"]
            for n in premios:
                print("     %d: R$ %s" % (n, premios[n]))
            continue

        # a chave 'numeros' está presente
        for res_nums in _numeros:
            print("  -")
            print("   concurso: %d" % result["concurso"])
            print("   numeros:", " ".join("%02d" % n for n in res_nums))
            print("   premios:")

            premios = result["premios"]
            for n in premios:
                print("     %d: R$ %s" % (n, premios[n]))

    if erros:
        if "result" in vars():
            print()
        print("  erros:", ", ".join(sorted(map(str, erros))))


def exec_conferir(
    loteria: loterica.Loteria, concursos: List[int], apostas: List[int]
) -> int:
    erros = set()
    try:
        resultados = iter_resultados(loteria.conferir, (concursos, apostas), erros)
    except loterica.LoteriaNaoSuportada as err:
        return error(
            "ERRO: conferência para '%s' não implementada" % err.args,
            show_help=False,
            code=6,
        )

    print("# conferência da", loteria.nome)
    print("%s:" % loteria.nome)

    for resp in resultados:
        print("  %d:" % resp[0]["concurso"])
        for r in resp:
            print("  - aposta:", end="")
            for n in r["numeros"]:
                if n in r["acertou"][0]:
                    print("", hi_acerto("%02d" % n), end="")
                else:
                    print(" %02d" % n, end="")
            print("\n    acertou:")
            for acertou, ganhou in zip(r["acertou"], r["ganhou"]):
                print("      %d: %s" % (len(acertou), hi_ganho("R$ " + ganhou)))

    if erros:
        if "resp" in vars():
            print()
        print("  erros:", ", ".join(sorted(map(str, erros))))


def __highlight_closure(
    color: int = 0, spec: int = 0, condition: Callable[[str], bool] = lambda x: True
) -> Callable[[str], str]:
    if sys.stdout.isatty():
        formatting = "\x1b[%02d;%02dm%%s\x1b[00m" % (spec, color)
        return lambda arg: formatting % arg if condition(arg) else arg
    else:
        return lambda arg: arg


# Função de destaque de número acertado
hi_acerto = __highlight_closure(color=33)

# Função de destaque de ganhos
hi_ganho = __highlight_closure(color=32, spec=0, condition=lambda x: x != "R$ 0,00")


def main(argv: List[str] = sys.argv, cfg_path: str = None) -> int:
    try:
        opts, args = getopt.gnu_getopt(
            argv[1:],
            # opções curtas
            "hn:q:c:i",
            # opções longas
            ["help", "numeros=", "quantidade=", "concurso=", "stdin"],
        )
    except getopt.GetoptError as err:
        return error("ERRO:", err, code=1)

    # Avalia os parâmetros passados
    numeros = None
    quantidade = None
    concursos: List[int] = []
    usar_stdin = False
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
            elif "-" in arg:
                faixa = arg.split("-")
                if len(faixa) != 2 or not (faixa[0].isdigit() and faixa[1].isdigit()):
                    return error("ERRO: faixa '%s' inválida" % arg)
                faixa = list(map(int, faixa))
                concursos.extend(range(faixa[0], faixa[1] + 1))
            else:
                concursos.append(-1)
        elif option in ("-i", "--stdin"):
            usar_stdin = True

    if len(args) < 1:
        return error("ERRO: deve ser informado uma loteria", code=2)

    nome = args[0]
    try:
        loteria = loterica.Loteria(nome.lower(), cfg_path=cfg_path)
    except loterica.LoteriaNaoSuportada:
        return error("ERRO: loteria '%s' não suportada" % nome, code=3)

    args = args[1:]
    if len(args) == 0 and usar_stdin:
        for linha in sys.stdin.readlines():
            if not linha.lstrip().startswith("#"):
                args.append(linha)

    apostas = []
    for arg in args:
        aposta = []
        for n in re.split("[, ]+", arg):
            fx = list(map(int, n.split("-", 1)))
            aposta.extend(range(fx[0], fx[-1] + 1))
        apostas.append(aposta)

    if concursos:
        if quantidade or numeros:
            return error("ERRO: parâmetros incompatíveis", code=4)
        elif apostas:
            return exec_conferir(loteria, concursos, apostas)
        else:
            return exec_consultar(loteria, concursos)
    elif len(apostas) > 0:
        return exec_conferir(loteria, [-1], apostas)
    else:
        return exec_gerar(loteria, quantidade or 1, numeros)


if __name__ == "__main__":
    sys.exit(main())
