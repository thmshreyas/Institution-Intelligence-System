class KeywordVerifier:

    def verify(self, text: str, keywords: list[str]):

        text = text.lower()

        matches = []

        for keyword in keywords:

            if keyword.lower() in text:

                matches.append(keyword)

        return {"passed": len(matches) > 0, "matches": matches}
