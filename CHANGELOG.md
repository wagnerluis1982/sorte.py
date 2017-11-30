# Changelog

Todas as mudanças de destaque nesse projeto será documentado neste arquivo. 

## [0.0.4] - 2017-11-29

### Modificado
- Nova estrutura do cache de forma a otimizar consultas, não é mais preciso repetir o _parse_ das páginas.
- Também guarda em cache as informações de consulta do último concurso.
- Apenas um banco de dados para o cache, com várias tabelas (com nomes diferentes para evitar colisão).

## [0.0.3] - 2017-11-26

### Adicionado
- Projeto convertido para Python 3.
- Arquivo de changelog.

### Modificado
- Usa 'entry_points' em vez de 'scripts' no `setup.py`.
- Correções de bugs e otimizações no sistema de cache.

## [0.0.2] - 2016-03-22

### Adicionado
- Aplicação renomeada para "sorte.py".
- Instalador (`setup.py`), com instruções para instalar via `pip` no README.
- Consulta de resultados dos sorteios.
- Conferência de apostas, via argumentos ou _stdin_.
- Descobrindo um caminho genérico para colocar o cache das páginas.
- Cache usando um arquivo SQLite.
- Identifica, na conferência de aposta, que deve-se obter o último resultado.
- Destaque dos ganhos obtidos, na conferência.

### Modificado
- Gerador lotomania: 20 números por padrão.
- Script refeito para ter saída mais bem formatada.
- 

## [0.0.1] - 2014-04-04

### Adicionado
- Gerador de números de Lotofácil, Lotomania, Mega Sena e Quina.
- Interface CLI em script para ser usado no shell.
