import os
import sys

from dotenv import load_dotenv

from src.verification.age_search import AgeSearch

load_dotenv()

api_key = os.getenv("SERPER_API_KEY")
if not api_key:
    print("Error: SERPER_API_KEY is not set in .env")
    sys.exit(1)

search = AgeSearch(api_key)
year = search.get_established_year("Anna University")
print(year)
