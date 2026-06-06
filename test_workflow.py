import os

from src.discovery.aishe_source import AisheDiscoverySource
from src.website.resolver import WebsiteResolver
from src.web.crawler import WebsiteCrawler

from src.verification.age_search import AgeSearch
from src.verification.engineering import EngineeringVerifier
from src.verification.mba import MBAVerifier
from src.verification.phd import PhDVerifier


from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERPER_API_KEY")
if not API_KEY:
    raise ValueError("SERPER_API_KEY is not set in .env")


def main():

    source = AisheDiscoverySource(
        "data/aishe.xlsx"
    )

    records = source.discover()

    # Test university
    university = records[10]

    print("\nUNIVERSITY")
    print(university)

    resolver = WebsiteResolver(
        API_KEY
    )

    website = resolver.resolve(
        university.name,
        university.state
    )

    print("\nWEBSITE")
    print(website)

    if not website:
        print("No website found")
        return

    url = website[1]

    crawler = WebsiteCrawler()

    text = crawler.crawl(url)

    # Prevent huge memory usage
    # text = text[:500000]

    print(
        "\nTEXT LENGTH:",
        len(text)
    )

    # ------------------
    # AGE EXTRACTION
    # ------------------

    age_search = AgeSearch(
        API_KEY
    )

    established_year = (
        age_search.get_established_year(
            university.name
        )
    )

    if established_year:

        age = (
            2026
            - established_year
        )

        age_result = {
            "passed": age >= 50,
            "year": established_year,
            "age": age
        }

    else:

        age_result = {
            "passed": False,
            "year": None,
            "age": None
        }

    # ------------------
    # PROGRAM VERIFICATION
    # ------------------

    engineering_result = (
        EngineeringVerifier()
        .verify(text)
    )

    mba_result = (
        MBAVerifier()
        .verify(text)
    )

    phd_result = (
        PhDVerifier()
        .verify(text)
    )

    # ------------------
    # OUTPUT
    # ------------------

    print("\nAGE")
    print(age_result)

    print("\nENGINEERING")
    print(engineering_result)

    print("\nMBA")
    print(mba_result)

    print("\nPHD")
    print(phd_result)

    eligible = (

        age_result["passed"]

        and

        engineering_result["passed"]

        and

        mba_result["passed"]

        and

        phd_result["passed"]

    )

    print("\nFINAL RESULT")

    print(
        "ELIGIBLE:",
        eligible
    )


if __name__ == "__main__":
    main()