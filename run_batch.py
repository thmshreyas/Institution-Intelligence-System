import pandas as pd

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

TARGET_QUALIFIED = int(os.getenv("TARGET_QUALIFIED", "5"))


def main():

    source = AisheDiscoverySource(
        "data/aishe.xlsx"
    )

    records = source.discover()

    resolver = WebsiteResolver(API_KEY)

    crawler = WebsiteCrawler()

    age_search = AgeSearch(API_KEY)

    all_results = []

    qualified_results = []

    qualified_count = 0

    total_processed = 0

    for university in records:

        if qualified_count >= TARGET_QUALIFIED:

            print(
                f"\nReached {TARGET_QUALIFIED} qualified universities."
            )

            break

        print(
            f"\n[{total_processed + 1}] Processing:",
            university.name
        )

        try:

            # --------------------
            # WEBSITE RESOLUTION
            # --------------------

            website = resolver.resolve(
                university.name,
                university.state
            )

            if not website:

                print(
                    "No website found."
                )

                continue

            url = website[1]

            # --------------------
            # WEBSITE CRAWLING
            # --------------------

            text = crawler.crawl(url)

            # limit crawler text
            text = text[:500000]

            # --------------------
            # AGE EXTRACTION
            # --------------------

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

                age_passed = (
                    age >= 50
                )

            else:

                age = None

                age_passed = False

            # --------------------
            # PROGRAM VERIFICATION
            # --------------------

            engineering = (
                EngineeringVerifier()
                .verify(text)
            )

            mba = (
                MBAVerifier()
                .verify(text)
            )

            phd = (
                PhDVerifier()
                .verify(text)
            )

            # --------------------
            # ELIGIBILITY
            # --------------------

            eligible = (

                age_passed

                and

                engineering["passed"]

                and

                mba["passed"]

                and

                phd["passed"]

            )

            row = {

                "name":
                    university.name,

                "state":
                    university.state,

                "website":
                    url,

                "established_year":
                    established_year,

                "age":
                    age,

                "engineering":
                    engineering["passed"],

                "mba":
                    mba["passed"],

                "phd":
                    phd["passed"],

                "eligible":
                    eligible

            }

            all_results.append(row)

            total_processed += 1

            print(
                "Eligible:",
                eligible
            )

            if eligible:

                qualified_results.append(
                    row
                )

                qualified_count += 1

                print(
                    f"Qualified Count: "
                    f"{qualified_count}"
                )

        except Exception as e:

            print(
                f"FAILED: {e}"
            )

    # --------------------
    # SAVE ALL RESULTS
    # --------------------

    all_df = pd.DataFrame(
        all_results
    )

    all_df.to_csv(
        "output/all_results.csv",
        index=False
    )

    # --------------------
    # SAVE QUALIFIED
    # --------------------

    qualified_df = pd.DataFrame(
        qualified_results
    )

    qualified_df.to_csv(
        "output/qualified_colleges.csv",
        index=False
    )

    print(
        "\n======================"
    )

    print(
        "Total Processed:",
        len(all_results)
    )

    print(
        "Qualified:",
        len(qualified_results)
    )

    print(
        "Saved:"
    )

    print(
        "output/all_results.csv"
    )

    print(
        "output/qualified_colleges.csv"
    )


if __name__ == "__main__":

    main()