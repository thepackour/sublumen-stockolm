from app.services.crawlers.base import BaseNewsCrawler
from app.services.crawlers.chosun import ChosunCrawler
from app.services.crawlers.general import GeneralCrawler
from app.services.crawlers.hankyung import HankyungCrawler


class CrawlerFactory:

    def __init__(self):
        self.crawlers = [
            HankyungCrawler(),
            ChosunCrawler()
        ]
        self.general_crawler = GeneralCrawler()

    def get_crawler(self, url: str) -> BaseNewsCrawler:
        for crawler in self.crawlers:
            if crawler.check_url(url):
                return crawler

        return self.general_crawler