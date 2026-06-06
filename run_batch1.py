import os
import sys

from dotenv import load_dotenv

from src.pipeline.batch_runner import run_batch_pipeline

load_dotenv()


def main():
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("Error: SERPER_API_KEY is not set. Copy .env.example to .env and add your key.")
        sys.exit(1)

    target_qualified = int(os.getenv("TARGET_QUALIFIED", "2"))
    aishe_path = os.getenv("AISHE_DATA_PATH", "data/AISHE.xlsx")

    result = run_batch_pipeline(
        api_key=api_key,
        target_qualified=target_qualified,
        aishe_path=aishe_path,
    )

    print(f"\nPipeline status: {result['status']}")
    print(f"Qualified colleges: {result['qualified_count']}")


if __name__ == "__main__":
    main()
