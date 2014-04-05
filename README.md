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

Loterias disponíveis por enquanto: duplasena, lotofacil, lotomania, megasena,
quina.

### Conferindo apostas

Ainda não implementado

### Consultando resultados

Ainda não implementado
