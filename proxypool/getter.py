from .utils import get_page
import re


class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def parse_page(self,pattern,html):
        if html:
            pattern = re.compile(pattern)
            ips = pattern.findall(html)
            return ips
        else:
            return None


    def crawl_89ip(self):
        for page in range(1,20):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(page)
            html = get_page(start_url)
            ips=self.parse_page("<tr><td>([\d\.]+?)</td><td>(.+?)</td><td>", html)
            for ip in ips:
                yield str(ip[0] + ":" + ip[1])

    def crawl_ip3366(self):
        for page in range(1, 15):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ips=self.parse_page("<tr><td>([\d\.]+?)</td><td>(.+?)</td><td>", html)
            for ip in ips:
                yield str(ip[0] + ":" + ip[1])

    def crawl_superfastip(self):
        for page in range(1, 10):
            start_url = 'http://www.superfastip.com/welcome/freeip/{}'.format(page)
            html = get_page(start_url)
            ips=self.parse_page("</td></tr><tr><td>([\d\.]+?)</td><td>(.+?)</td><!--<td>",html)
            for ip in ips:
                yield str(ip[0] + ":" + ip[1])


    # def crawl_xicidaili(self):
    #     for page in range(1, 15):
    #         start_url = 'https://www.xicidaili.com/nn/{}'.format(page)
    #         html = get_page(start_url)
    #         ips=self.parse_page('alt="Cn"/></td><td>(.+?)</td><td>(.+?)</td><td>',html)
    #         print(ips)
    #         for ip in ips:
    #             yield str(ip[0] + ":" + ip[1])

    def crawl_66ip(self):
        for page in range(1,15):
            start_url = 'http://www.66ip.cn/{}.html'.format(page)
            html = get_page(start_url)
            ips=self.parse_page("</td></tr><tr><td>(.+?)</td><td>(.+?)</td><td>",html)
            print(ips)
            for ip in ips:
                yield str(ip[0] + ":" + ip[1])


