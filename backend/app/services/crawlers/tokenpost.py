from bs4 import BeautifulSoup

from app.services.crawlers.base import BaseNewsCrawler


class TokenpostCrawler(BaseNewsCrawler):

    def check_url(self, url: str) -> bool:
        return "tokenpost.kr" in url

    def get_article(self, url: str) -> str:
        response = self.session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        return soup.select_one(".article_content").get_text("\n", strip=True)
