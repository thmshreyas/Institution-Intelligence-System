from src.website.search import SerperSearch
from src.website.ranking import score_result


class WebsiteResolver:

    def __init__(self, api_key):

        self.search = SerperSearch(api_key)

    def resolve(
        self,
        institution_name,
        state=None,
    ):

        query = (
            f"{institution_name} "
            f"{state or ''} "
            f"official website"
        )

        results = self.search.search(query)

        candidates = []

        for item in results.get(
            "organic",
            []
        ):

            score = score_result(
                institution_name,
                item.get("title"),
                item.get("link"),
                item.get("snippet"),
                item.get(
                    "position",
                    100
                ),
            )

            candidates.append(
                (
                    score,
                    item.get("link"),
                    item.get("title"),
                )
            )

        candidates.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        if not candidates:
            return None

        return candidates[0]