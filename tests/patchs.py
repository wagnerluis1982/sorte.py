from dataclasses import replace


# modifica o método privado Loteria._url para garantir que use o script CGI interno
def loteria_class() -> None:
    if not getattr(loteria_class, "done", False):
        # garantie que servidor interno de fixtures está inicializado
        import fixtures

        fixtures.start_server()

        # faz o patch
        import sortepy.loterica

        __patch_url_method(sortepy.loterica.Loteria._url, fixtures.server_url)
        __patch_settings(sortepy.loterica.LOTERIAS)

        # marca que o patch já foi feito
        loteria_class.done = True


def __patch_url_method(_url: str, server_url: str) -> None:
    _url.__defaults__ = (
        server_url + "/cgi-bin/",  # base
        "obter-loteria.py",  # script
        "?nome=%(loteria)s&concurso=%(concurso)s",  # query
    )


def __patch_settings(loterias: dict) -> None:
    for key, value in loterias.items():
        loterias[key] = replace(value, url_script=None)
