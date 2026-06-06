from src.verification.age import (
    AgeVerifier
)

verifier = AgeVerifier()

print(
    verifier.verify(
        1970
    )
)