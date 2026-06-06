from src.verification.keyword_verifier import KeywordVerifier

PHD_KEYWORDS = [
    "phd",
    "doctoral",
    "doctor of philosophy",
    "research programme",
    "research program",
]


class PhDVerifier:

    def __init__(self):

        self.verifier = KeywordVerifier()

    def verify(self, text):

        return self.verifier.verify(text, PHD_KEYWORDS)
