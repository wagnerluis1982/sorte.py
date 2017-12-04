# modifica o método privado Loteria._url para garantir que use o script CGI interno
def loteria_class():
    if not loteria_class.done:
        # garantie que servidor interno de fixtures está inicializado
        import fixtures
        fixtures.start_server()

        # faz o patch
        import sortepy.loterica
        sortepy.loterica.Loteria._url.__defaults__ = (
            fixtures.server_url + '/cgi-bin/',         # base
            'obter-loteria.py',                        # script
            '?nome=%(loteria)s&concurso=%(concurso)s'  # query
        )
        del sortepy.loterica.LOTERIAS['lotomania']['url-script']
        # marca que o patch já foi feito
        loteria_class.done = True


loteria_class.done = False
