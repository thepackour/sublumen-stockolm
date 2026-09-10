import json
import re

import requests
from bs4 import BeautifulSoup

url = "https://biz.chosun.com/stock/stock_general/2026/08/06/2SE2G2FEXZAEVJSBHA5WTIRL2E/?utm_source=naver&utm_medium=original&utm_campaign=biz"

header = ({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
})

res = requests.get(url, headers=header)

print(res.status_code)

soup = BeautifulSoup(res.text, "html.parser")

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

    print(content)