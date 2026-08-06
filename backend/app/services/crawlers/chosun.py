import json
import re

from bs4 import BeautifulSoup

from app.services.crawlers.base import BaseNewsCrawler


class ChosunCrawler(BaseNewsCrawler):

    def check_url(self, url: str) -> bool:
        return "chosun.com" in url

    def get_article(self, url: str) -> str:
        response = self.session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        script = soup.select_one("#fusion-metadata").text

        match = re.search(
            r'Fusion\.globalContent=(\{.*?\});',
            script,
            re.DOTALL
        )

        if match:
            json_text = match.group(1)
            data = json.loads(json_text)

            content = "\n".join(
                item["content"]
                for item in data["content_elements"]
                if item["type"] == "text"
            )

            return content
        return None

# biz.chosun.com의 경우 본문에 주식 이름과 심볼이 들어있다는 점 참고