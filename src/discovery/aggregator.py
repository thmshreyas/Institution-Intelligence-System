# src/discovery/aggregator.py

from src.discovery.aishe_source import AisheDiscoverySource
from src.discovery.wikipedia_source import WikipediaDiscoverySource


class DiscoveryAggregator:

    def __init__(self, aishe_file):

        self.aishe = AisheDiscoverySource(aishe_file)

        self.wikipedia = WikipediaDiscoverySource()

    def discover(self):

        records = []

        records.extend(self.aishe.discover())

        records.extend(self.wikipedia.discover())

        seen = set()
        unique = []

        for r in records:

            key = r.name.lower().replace(",", "").strip()

            if key not in seen:
                seen.add(key)
                unique.append(r)

        return unique
