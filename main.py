import os

import pandas as pd
from dotenv import load_dotenv

from src.discovery.aggregator import DiscoveryAggregator

load_dotenv()

aishe_path = os.getenv("AISHE_DATA_PATH", "data/AISHE.xlsx")

aggregator = DiscoveryAggregator(aishe_path)

records = aggregator.discover()

print(f"\nTotal Institutions Found: {len(records)}\n")

for r in records[:20]:
    print(r)

# Save output
df = pd.DataFrame([
    {
        "name": r.name,
        "state": r.state,
        "source": r.source
    }
    for r in records
])

df.to_csv(
    "output/discovered_institutions.csv",
    index=False
)

print("\nSaved to output/discovered_institutions.csv")