from bs4 import BeautifulSoup

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
        response = self.session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for target in targets:
            return soup.select_one(target).get_text("\n", strip=True)

        return None