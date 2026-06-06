import os
import sys

from dotenv import load_dotenv

from src.website.resolver import WebsiteResolver

load_dotenv()

api_key = os.getenv("SERPER_API_KEY")
if not api_key:
    print("Error: SERPER_API_KEY is not set in .env")
    sys.exit(1)

resolver = WebsiteResolver(api_key)

tests = [
    ("Anna University", "Tamil Nadu"),
    ("University of Mumbai", "Maharashtra"),
    ("Utkal University", "Odisha"),
]

for name, state in tests:
    result = resolver.resolve(name, state)
    print()
    print(name)
    print(result)
