# encoding=utf8

import codecs
import cookielib
import os
import re
import urllib2


def get_config_path(app='sortepy'):
    """Obtém o caminho de configuração de acordo com o SO

    Por enquanto é suportado os sistemas POSIX e Windows (NT)
    """
    # Linux, UNIX, BSD, ...
    if os.name == 'posix':
        prefixo = '.config/'
        profile_dir = os.environ.get("HOME")

    # Windows 2000, XP, Vista, 7, 8, ...
    elif os.name == 'nt':
        prefixo = ''
        profile_dir = os.environ.get("APPDATA")

    # Se nenhum SO suportado foi detectado, lança uma exceção
    else:
        raise NotImplementedError("Caminho de configuração não detectado")

    return os.path.join(profile_dir, prefixo + app)


class Util(object):
    def __init__(self, cfg_path=None):
        self.usar_cache = False
        if cfg_path:
            try:
                cfg_path = os.path.realpath(cfg_path) or get_config_path()
            except NotImplementedError:
                pass
            else:
                self.cfg_path = cfg_path
                self.pages_cache = os.path.join(cfg_path, 'cache', 'paginas')
                self.usar_cache = True

    def download(self, url, usar_cache=False):
        usar_cache = usar_cache or self.usar_cache

        # Obtém a página do cache
        conteudo = None
        if usar_cache:
            conteudo = self.cache(url)

        # Ou faz o download
        if conteudo is None:
            # As páginas de resultado de loterias exigem cookies
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            # A adição desse cookie dobra o tempo de resposta
            opener.addheaders.append(("Cookie", "security=true"))

            page = opener.open(url)
            conteudo = page.read()

            charset = page.headers.getparam('charset')
            if charset is not None:
                try:
                    conteudo = unicode(conteudo, charset)
                except (UnicodeDecodeError, LookupError):
                    pass

            if usar_cache:
                self.cache(url, conteudo)

        return conteudo

    def cache(self, url, conteudo=None):
        # Caminho com nome seguro
        caminho = os.path.join(self.pages_cache, re.sub('[:/?]', '_', url))

        # Sem contéudo: leitura do cache
        if conteudo is None:
            try:
                f = codecs.open(caminho, 'r', encoding='utf-8')
            except IOError:
                return None
            else:
                conteudo = f.read()
                f.close()
                return conteudo

        # Do contrário: escrita no cache
        else:
            f = codecs.open(caminho, 'w', encoding='utf-8')
            f.write(conteudo)
            f.close()
