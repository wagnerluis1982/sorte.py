# encoding=utf8
import cookielib
import os
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
        self.cfg_path = os.path.realpath(cfg_path) or get_config_path()

    def download(url):
        # As páginas de resultado de loterias exigem cookies
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        # A adição desse cookie dobra o tempo de resposta
        opener.addheaders.append(("Cookie", "security=true"))

        page = opener.open(url)
        page_data = page.read()

        charset = page.headers.getparam('charset')
        if charset is not None:
            try:
                return unicode(page_data, charset)
            except (UnicodeDecodeError, LookupError):
                pass
        else:
            return page_data
