sorte.py
========

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

Para instalar, basta baixar o projeto, descompactar e executar, estando no
diretório do projeto

    $ python3 setup.py install

Ou, você pode executar o `pip` diretamente

    $ pip3 install git+https://github.com/wagnerluis1982/sorte-py

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
