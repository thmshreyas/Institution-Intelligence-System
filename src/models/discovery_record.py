# discovery_record.py

from dataclasses import dataclass


@dataclass
class DiscoveryRecord:

    name: str

    state: str | None = None

    source: str = ""

    year_of_establishment: int | None = None
