import requests


class SerperSearch:

    _cache = {}

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, query: str):

        if query in self._cache:

            print(f"[CACHE HIT] {query}")

            return self._cache[query]

        print(f"[SERPER CALL] {query}")

        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
            },
            json={
                "q": query,
                "num": 10,
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        self._cache[query] = data

        return data