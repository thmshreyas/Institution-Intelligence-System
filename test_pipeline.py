from src.pipeline.pipeline import (
    VerificationPipeline
)

pipeline = (
    VerificationPipeline()
)

result = pipeline.run(
    "https://www.bietdvg.edu"
)

print(result)