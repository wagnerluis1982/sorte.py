# encoding=utf8
import cookielib
import urllib2


class Util(object):
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
