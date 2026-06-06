import os

import pandas as pd

from src.collectors.address_collector import AddressCollector
from src.collectors.leadership_collector import LeadershipCollector
from src.discovery.aishe_source import AisheDiscoverySource
from src.scoring.confidence_scorer import ConfidenceScorer
from src.verification.age_search import AgeSearch
from src.verification.engineering import EngineeringVerifier
from src.verification.mba import MBAVerifier
from src.verification.phd import PhDVerifier
from src.web.crawler import WebsiteCrawler
from src.website.resolver import WebsiteResolver


def save_markdown_report(row: dict) -> None:
    os.makedirs("output/reports", exist_ok=True)

    filename = (
        row["name"]
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )

    filepath = f"output/reports/{filename}.md"

    report = f"""# {row['name']}

## Basic Information

- Website: {row['website']}
- State: {row['state']}
- Established Year: {row['established_year']}
- Age: {row['age']}

## Qualification Criteria

- Engineering: {row['engineering']}
- MBA: {row['mba']}
- PhD: {row['phd']}
- Eligible: {row['eligible']}

## Leadership

{row['vice_chancellor']}

## Address

{row['address']}

## Confidence Score

{row['confidence']}/100
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)


def run_batch_pipeline(
    api_key: str,
    target_qualified: int = 20,
    aishe_path: str = "data/AISHE.xlsx",
    current_year: int = 2026,
) -> dict:
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/reports", exist_ok=True)

    source = AisheDiscoverySource(aishe_path)
    records = source.discover()

    resolver = WebsiteResolver(api_key)
    crawler = WebsiteCrawler()
    age_search = AgeSearch(api_key)
    leadership_collector = LeadershipCollector()
    address_collector = AddressCollector()
    scorer = ConfidenceScorer()

    all_results = []
    qualified_results = []
    qualified_count = 0

    for university in records:
        if qualified_count >= target_qualified:
            break

        print(f"\nProcessing: {university.name}")

        try:
            website = resolver.resolve(university.name, university.state)

            if not website:
                continue

            url = website[1]
            text = crawler.crawl(url)
            text = text[:500000]

            established_year = age_search.get_established_year(university.name)

            if established_year:
                age = current_year - established_year
                age_passed = age >= 50
            else:
                age = None
                age_passed = False

            engineering = EngineeringVerifier().verify(text)
            mba = MBAVerifier().verify(text)
            phd = PhDVerifier().verify(text)

            vice_chancellor = leadership_collector.collect(text)
            address = address_collector.collect(text)

            eligible = (
                age_passed
                and engineering["passed"]
                and mba["passed"]
                and phd["passed"]
            )

            row = {
                "name": university.name,
                "state": university.state,
                "website": url,
                "established_year": established_year,
                "age": age,
                "engineering": engineering["passed"],
                "mba": mba["passed"],
                "phd": phd["passed"],
                "vice_chancellor": vice_chancellor,
                "address": address,
                "eligible": eligible,
            }
            row["confidence"] = scorer.score(row)

            all_results.append(row)

            if eligible:
                qualified_results.append(row)
                qualified_count += 1
                save_markdown_report(row)
                print(f"Qualified: {qualified_count}")

            if len(all_results) % 10 == 0:
                pd.DataFrame(all_results).to_csv(
                    "output/checkpoint.csv",
                    index=False,
                )

        except Exception as e:
            print(f"FAILED: {e}")

    pd.DataFrame(all_results).to_csv("output/all_results.csv", index=False)
    pd.DataFrame(qualified_results).to_csv(
        "output/qualified_colleges.csv",
        index=False,
    )

    print("\nDone.")
    print(f"Qualified Colleges: {len(qualified_results)}")

    return {
        "status": "completed",
        "qualified_count": len(qualified_results),
    }
