from urllib.parse import urlparse

BAD_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "wikipedia.org",
    "collegedunia.com",
    "shiksha.com",
    "careers360.com",
]


BAD_WORDS = [
    "admission",
    "login",
    "department",
    "departments",
    "course",
    "results",
]


def score_result(
    institution_name,
    title,
    url,
    snippet,
    position,
):

    score = 0

    title = (title or "").lower()
    url = (url or "").lower()
    snippet = (snippet or "").lower()

    institution_name = institution_name.lower().replace(",", "")

    # Google ranking matters
    score += max(0, 30 - (position * 2))

    # Title match
    if institution_name in title:
        score += 100

    # URL match
    tokens = institution_name.split()

    for token in tokens:

        if len(token) < 4:
            continue

        if token in url:
            score += 10

    # Education domains
    if ".ac.in" in url:
        score += 50

    if ".edu" in url:
        score += 30

    # Bad domains
    for bad in BAD_DOMAINS:

        if bad in url:
            score -= 100

    # Bad URLs
    for bad in BAD_WORDS:

        if bad in url:
            score -= 30

    # Good snippet signals
    if "university" in snippet:
        score += 20

    if "engineering" in snippet:
        score += 10

    return score
