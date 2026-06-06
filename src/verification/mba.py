from src.verification.keyword_verifier import KeywordVerifier

MBA_KEYWORDS = [
    "mba",
    "management studies",
    "business administration",
    "school of management",
]


class MBAVerifier:

    def __init__(self):

        self.verifier = KeywordVerifier()

    def verify(self, text: str):

        return self.verifier.verify(text, MBA_KEYWORDS)
