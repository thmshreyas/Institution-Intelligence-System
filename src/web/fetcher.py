import requests

from bs4 import BeautifulSoup


class WebsiteFetcher:

    def fetch_text(self, url: str):

        try:

            response = requests.get(
                url, timeout=20, headers={"User-Agent": "Mozilla/5.0"}
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            return soup.get_text(" ", strip=True)

        except Exception as e:

            print(f"Fetch Error: {url}", e)

            return ""
