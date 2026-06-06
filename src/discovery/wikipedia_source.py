import requests
import pandas as pd
from io import StringIO

from src.models.discovery_record import DiscoveryRecord


class WikipediaDiscoverySource:

    URL = "https://en.wikipedia.org/wiki/" "List_of_universities_in_India"

    def discover(self):

        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(self.URL, headers=headers, timeout=20)

        tables = pd.read_html(StringIO(response.text))

        records = []

        for table in tables:

            for col in table.columns:

                if "university" in str(col).lower():

                    for value in table[col].dropna():

                        records.append(
                            DiscoveryRecord(name=str(value).strip(), source="Wikipedia")
                        )

                    break

        return records
