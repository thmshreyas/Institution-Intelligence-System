from src.verification.keyword_verifier import KeywordVerifier

ENGINEERING_KEYWORDS = [
    "engineering",
    "b.tech",
    "btech",
    "m.tech",
    "mtech",
]


class EngineeringVerifier:

    def __init__(self):

        self.verifier = KeywordVerifier()

    def verify(self, text: str):

        return self.verifier.verify(text, ENGINEERING_KEYWORDS)
