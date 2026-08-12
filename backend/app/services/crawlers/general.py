import requests
from bs4 import BeautifulSoup

from app.core.logger import logger
from app.services.crawlers.base import BaseNewsCrawler

targets = [
    "#articletxt",
    "#articleBody",
    "#cont_newstext",
    ".article_content",
    ".news_body"
]

class GeneralCrawler(BaseNewsCrawler):

    def check_url(self, url: str) -> bool:
        return True

    def get_article(self, url: str) -> str:
        try:
            response = self.session.get(url, timeout=10)
        except requests.exceptions.ConnectTimeout:
            logger.warning(
                "뉴스 API: ConnectTimeout (%s)",
                url,
            )
            return None
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for target in targets:
            selected = soup.select_one(target)
            if selected is None: continue
            article = selected.get_text("\n", strip=True)
            return article

        return None