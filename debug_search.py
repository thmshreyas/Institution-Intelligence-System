from src.website.search import WebsiteSearch

search = WebsiteSearch()

results = search.search(
    "Anna University"
)

for r in results[:10]:
    print(r)