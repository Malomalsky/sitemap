import re
import ssl
import urllib.request
from datetime import datetime
from multiprocessing.pool import ThreadPool
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse, urlsplit, urlunsplit


class Crawler:
    MAX_LINKS = 50000

    def __init__(self, url,  threads, silence=False):
        self.url = self.normalize(url)
        self.host = urlparse(self.url).netloc
        self.threads = threads
        self.silence = silence
        self.founded_links = []
        self.visited_links = [self.url]
        self.output = f"../sitemaps/{urlparse(self.url).netloc}-sitemap.xml"

        # Для возможности парсинга https.
        my_ssl = ssl.create_default_context()
        my_ssl.check_hostname = False
        my_ssl.verify_mode = ssl.CERT_NONE

        self.my_ssl = my_ssl

    # Кравлер соответсвует протоколу последовательности - для удобства работы с классом.
    def __len__(self):
        return len(self.founded_links)

    def __iter__(self):
        return iter(self.founded_links)

    def __getitem__(self, index):
        return self.founded_links[index]

    def _crawl(self, url):
        """
        Основной процесс класса. \n
        Поиск всех линков на сайте.
        """
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        if len(self.founded_links) <= Crawler.MAX_LINKS:
            if not self.silence:
                print(f"{len(self.founded_links)} - Парсинг {url}")

            try:
                response = urllib.request.urlopen(req, context=self.my_ssl)

            except HTTPError:
                print('Превышен лимит запросов.')
                return self.founded_links
            except:
                return

            founded_links = self.find_links(response)
            links = []

            # Фильтрация полученных URl.
            for link in founded_links:
                if 'infinite' in link:
                    pass

                elif Crawler.is_url(link) and self.is_internal(link):
                    links.append(link) if (link not in links) else None
                    self.founded_links.append(link) if (link not in self.founded_links) else None

            # Исследование найденных URL с мультипроцессингом.
            scrap_pool = ThreadPool(self.threads)
            scrap_pool.map(self.link_analyze, links)
            if len(self.founded_links) > 50000:
                scrap_pool.terminate()
                scrap_pool.join()

    def run(self):
        """
        Запуска кравлера.
        """
        self._crawl(self.url)
        return self.founded_links

    def is_internal(self, url):
        """
        Проверка принадлежности URL к исследуемому домену.
        """
        host = urlparse(url).netloc
        return host == self.host or host == ''

    def link_analyze(self, link):
        if link not in self.visited_links:
            link = self.normalize(link)
            self.visited_links.append(link)
            self._crawl(urljoin(self.url, link))

    @staticmethod
    def find_links(response):
        """
        Поиск url-ов на странице.
        """
        page = str(response.read())
        pattern = '<a [^>]*href=[\'|"](.*?)[\'"].*?>'
        founded_links = found_links = re.findall(pattern, page)
        return found_links

    @staticmethod
    def is_url(url):
        """
        Проверка корректности url.
        """
        scheme, netloc, path, qs, anchor = urlsplit(url)
        return url != '' and scheme in ['http', 'https', '']

    @staticmethod
    def normalize(url):
        """
        Нормализует полученный url.
        """
        scheme, netloc, path, qs, anchor = urlsplit(url)
        return urlunsplit((scheme, netloc, path, qs, anchor))


