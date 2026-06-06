import pandas as pd

from src.models.discovery_record import DiscoveryRecord


class AisheDiscoverySource:

    def __init__(self, file_path):
        self.file_path = file_path

    def discover(self):

        # Actual headers start from row 2
        df = pd.read_excel(self.file_path, header=2)

        # Clean column names
        df.columns = df.columns.astype(str).str.strip()

        print("\nColumns Found:")
        print(df.columns.tolist())

        records = []

        universities = df[
            ["University Name", "State", "University Type", "Year Of Establishment"]
        ].dropna(subset=["University Name"])

        universities = universities.drop_duplicates(subset=["University Name"])

        for _, row in universities.iterrows():

            year = row["Year Of Establishment"]

            # Clean establishment year
            if pd.isna(year):

                year = None

            elif str(year).strip() in ["-", "", "nan"]:

                year = None

            else:

                try:
                    year = int(float(year))

                except Exception:
                    year = None

            records.append(
                DiscoveryRecord(
                    name=str(row["University Name"]).strip(),
                    state=str(row["State"]).strip(),
                    source="AISHE",
                    year_of_establishment=year,
                )
            )

        print(f"\nUniversities Found: {len(records)}")

        return records
