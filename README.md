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

Para instalar, basta baixar o projeto, descompactar e executar, estando no
diretório do projeto

    $ python setup.py install

Ou, você pode executar o `pip` diretamente

    $ pip install git+https://github.com/wagnerluis1982/sorte-py

Modo de uso
-----------

### Gerando números para aposta

Para ter *uma* aposta gerada, na quantidade padrão da Quina, por exemplo, basta

    $ sorte.py quina

Outras opções disponíveis para geração:

    -q --quantidade   Quantas apostas deverão ser geradas. Padrão: 1
    -n --numeros      Quantos números cada aposta gerada terá. Se não informado
                        o padrão depende da LOTERIA informada
    -h --help         Mostra esta ajuda e finaliza

Loterias disponíveis: duplasena, lotofacil, lotomania, megasena, quina.

### Conferindo apostas

**ATENÇÃO**: Ainda não implementado. Esta é a interface proposta.

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

    $ sorte.py quina [-c 1325] -i
    1,23,39,44,50
    5 9 15 50 75
    1-3 30 56

O parâmetro `-i` admite um nome de arquivo como argumento, assim os dois
comandos abaixo são equivalentes.

    $ sorte.py quina -c 1325 -i < fezinha-na-quina.txt
    $ sorte.py quina -c 1325 -i fezinha-na-quina.txt

As linhas que iniciam por `#` são consideradas comentários.

### Consultando resultados

**ATENÇÃO**: Ainda não implementado. Esta é a interface proposta.

Para consultar, execute

    $ sorte.py quina -c|--concurso NUM

onde o argumento NUM é o número do concurso em que quer o resultado. Se quiser
obter o último resultado disponível, basta passar um argumento vazio, conforme
comando abaixo.

    $ sorte.py quina -c=
