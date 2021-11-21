sorte.py
========

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sorte.py)
[![PyPI](https://img.shields.io/pypi/v/sorte.py)](https://pypi.org/project/sorte.py)

> AVISO
> -----
>
> `sorte.py` não consegue fazer mais consultas (o que também afeta as conferências),
> desde que a Caixa mudou drasticamente o sistema. Este problema está sendo investigado.
>
> Veja https://github.com/wagnerluis1982/sorte.py/pull/4

Sobre
-----

O `sorte.py` é um script Python de linha de comando para geração e conferência
de apostas de loterias.  Surgiu com o propósito principal de conferir apostas
feitas nas Casas Lotéricas do Brasil.

A geração de números é como a *surpresinha*, mas os jogos têm que ser
preenchidos manualmente.

Instalação
----------

AVISO: `sorte.py` requer no mínimo o Python 3 para a instalação com sucesso.

Para instalar, basta executar o `pip` pondo como argumento o repositório.

    $ pip3 install git+https://github.com/wagnerluis1982/sorte-py

Licença
-------

O código fonte é licenciado sob a licença [GPLv3].

[GPLv3]: http://licencas.softwarelivre.org/gpl-3.0.pt-br.html

Modo de uso
-----------

### Gerando números para aposta

Para ter *uma* aposta gerada, na quantidade padrão da Quina, por exemplo, basta

    $ sorte.py quina

#### Todas as opções de geração

    -q --quantidade   Quantas apostas deverão ser geradas. Padrão: 1
    -n --numeros      Quantos números cada aposta gerada terá. Se não informado
                        o padrão depende da LOTERIA informada
    -h --help         Mostra esta ajuda e finaliza

Loterias disponíveis: duplasena, lotofacil, lotomania, megasena, quina.

### Conferindo apostas

Para conferir três apostas do último concurso, execute

    $ sorte.py quina '1,23,39,44,50' '5 9 15 50 75' '1-3 30 56'

Cada argumento é uma aposta. Os números podem ser separados por vírgula ou
espaço em branco. Caso utilize hífens entre dois números, será considerado um
intervalo.

Se for preciso especificar o concurso, então basta utilizar o parâmetro
`-c|--concurso`, conforme exemplo abaixo

    $ sorte.py quina -c 1325 '1,23,39,44,50' '5 9 15 50 75'

Caso o parâmetro `-i|--stdin` seja ativado, as apostas serão lidas da entrada
padrão, uma por linha até encontrar o EOF (Ctrl-D no Linux).

    $ sorte.py quina -c 1325 -i
    1,23,39,44,50
    5 9 15 50 75
    1-3 30 56

Com o parâmetro `-i`, fica possível a utilização de um arquivo com as apostas,
conforme exemplo.

    $ sorte.py quina -c 1325 -i < fezinha-na-quina.txt

As linhas que iniciam por `#` são consideradas comentários.

#### Conferindo vários concursos

O script permite conferir vários concursos de uma vez, passando o argumento `-c`
várias vezes

    $ sorte.py duplasena -c 1130 -c 1131 -i < minhas_apostas.txt

ou informar uma faixa de valores

    $ sorte.py quina -c 1325-1330 -i < fezinha.txt

#### Todas as opções de conferência

    -c --concurso     Número do concurso para consultar ou conferir. Pode ser
                        passada várias vezes
    -i --stdin        Recebe as apostas da entrada padrão, útil para manter as
                        apostas em um arquivo

### Consultando resultados

Para consultar, execute

    $ sorte.py JOGO -c|--concurso NUM

onde o argumento `NUM` é o número do concurso em que quer o resultado. Se quiser
obter o último resultado disponível, basta passar um argumento vazio, conforme
comando abaixo.

    $ sorte.py lotofacil -c=

#### Consultando vários concursos

Semelhante à conferência, é possível consultar vários concursos de uma vez:

    $ sorte.py duplasena -c 1130 -c 1131
    $ sorte.py duplasena -c 1136-1145

#### Todas as opções de consulta

    -c --concurso     Número do concurso para consultar ou conferir. Pode ser
                        passada várias vezes
