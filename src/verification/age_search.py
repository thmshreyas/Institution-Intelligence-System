import re

from src.website.search import SerperSearch
from collections import Counter

class AgeSearch:

    def __init__(self, api_key):
        self.search = SerperSearch(api_key)

    def get_established_year(
        self,
        institution_name
    ):

        query = (
            f"{institution_name} established year"
        )

        result = self.search.search(query)

        text = ""

        # Knowledge Graph (best source)
        if "knowledgeGraph" in result:

            kg = result["knowledgeGraph"]

            text += str(kg)

        # Organic results snippets
        for item in result.get(
            "organic",
            []
        ):

            text += (
                " "
                + item.get(
                    "snippet",
                    ""
                )
            )

        years = re.findall(
            r"(18\d{2}|19\d{2}|20\d{2})",
            text
        )

        if not years:
            return None

        years = [
            int(y)
            for y in years
        ]
        year_counts = Counter(years)

        # Return oldest reasonable year
        return year_counts.most_common(1)[0][0]