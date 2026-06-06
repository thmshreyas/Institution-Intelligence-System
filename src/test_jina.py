from googlesearch import search
import requests

college_name = "Anna University"

# Step 1: Search Google
query = f"{college_name} official website"

print(f"Searching for: {query}")

results = list(search(query, num_results=5))

if not results:
    print("No results found")
    exit()

# Step 2: Get first result
website = results[0]

print(f"\nWebsite Found: {website}")

# Step 3: Fetch content using Jina Reader
jina_url = f"https://r.jina.ai/http://{website.replace('https://', '').replace('http://', '')}"

print(f"\nFetching content from:")
print(jina_url)

response = requests.get(jina_url, timeout=60)

if response.status_code == 200:
    content = response.text

    print("\n===== PAGE CONTENT =====\n")
    print(content[:5000])  # first 5000 chars
else:
    print(f"Failed: {response.status_code}")