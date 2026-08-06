from abc import abstractmethod

import requests
from bs4 import BeautifulSoup

class BaseNewsCrawler:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        })

    @abstractmethod
    def get_article(self, url: str) -> str:
        pass

    @abstractmethod
    def check_url(self, url: str) -> bool:
        pass