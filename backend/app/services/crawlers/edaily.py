from bs4 import BeautifulSoup

from app.services.crawlers.base import BaseNewsCrawler


class EdailyCrawler(BaseNewsCrawler):

    def check_url(self, url: str) -> bool:
        return "edaily.co.kr" in url

    def get_article(self, url: str) -> str:
        response = self.session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        article = soup.select_one(".news_body").get_text("\n", strip=True)

        return "\n".join(article.split("]")[1:])
