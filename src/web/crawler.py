import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin, urlparse


class WebsiteCrawler:

    def crawl(self, base_url, max_pages=15):

        visited = set()

        texts = []

        try:

            response = requests.get(
                base_url, timeout=20, headers={"User-Agent": "Mozilla/5.0"}
            )

            soup = BeautifulSoup(response.text, "html.parser")

            domain = urlparse(base_url).netloc

            links = []

            for tag in soup.find_all("a", href=True):

                url = urljoin(base_url, tag["href"])

                if urlparse(url).netloc == domain:

                    links.append(url)

            links = links[:max_pages]

            for url in links:

                try:

                    page = requests.get(url, timeout=10)

                    page_soup = BeautifulSoup(page.text, "html.parser")

                    texts.append(page_soup.get_text(" ", strip=True))

                except:
                    pass

            return "\n".join(texts)

        except:
            return ""
