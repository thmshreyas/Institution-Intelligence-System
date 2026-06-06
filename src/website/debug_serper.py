import json
import os
import sys

from dotenv import load_dotenv

from src.website.search import SerperSearch

load_dotenv()

api_key = os.getenv("SERPER_API_KEY")
if not api_key:
    print("Error: SERPER_API_KEY is not set in .env")
    sys.exit(1)

search = SerperSearch(api_key)
result = search.search("Anna University Chennai official website")
print(json.dumps(result, indent=2))
