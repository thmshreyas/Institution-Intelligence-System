from dataclasses import dataclass


@dataclass
class InstitutionProfile:

    name: str

    state: str | None = None

    website: str | None = None

    engineering: bool = False

    mba: bool = False

    phd: bool = False

    established_year: int | None = None
