import json
import os
import re
from pathlib import Path

import pandas as pd

from src.llm.report_parser import parse_report_locally
from src.llm.report_refiner import refine_report
from src.pipeline.batch_runner import run_batch_pipeline
from src.scoring.confidence_scorer import ConfidenceScorer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUALIFIED_CSV = PROJECT_ROOT / "output" / "qualified_colleges.csv"
ALL_RESULTS_CSV = PROJECT_ROOT / "output" / "all_results.csv"
REPORTS_DIR = PROJECT_ROOT / "output" / "reports"
REFINED_DIR = REPORTS_DIR / "refined"


def _report_filename(name: str) -> str:
    return (
        name.replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )


def _to_str(value) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    return text or None


def _normalize_row(row: dict) -> dict:
    normalized = {
        "name": _to_str(row.get("name")) or "",
        "state": _to_str(row.get("state")),
        "website": _to_str(row.get("website")),
        "established_year": _to_int(row.get("established_year")),
        "age": _to_int(row.get("age")),
        "engineering": _to_bool(row.get("engineering")),
        "mba": _to_bool(row.get("mba")),
        "phd": _to_bool(row.get("phd")),
        "vice_chancellor": _to_str(row.get("vice_chancellor")),
        "address": _to_str(row.get("address")),
        "eligible": _to_bool(row.get("eligible")),
    }

    confidence = row.get("confidence")
    if confidence is None or (isinstance(confidence, float) and pd.isna(confidence)):
        normalized["confidence"] = ConfidenceScorer().score(normalized)
    else:
        normalized["confidence"] = int(confidence)

    return normalized


def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}


def _to_int(value) -> int | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    df = pd.read_csv(path)
    return [_normalize_row(row) for row in df.to_dict(orient="records")]


def _find_institution(name: str) -> dict | None:
    for path in (QUALIFIED_CSV, ALL_RESULTS_CSV):
        for row in _load_csv(path):
            if row["name"].lower() == name.lower():
                return row
    return None


def _extract_report_title(content: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _parse_report_basics(content: str) -> dict:
    basics = {
        "state": None,
        "confidence": 0,
        "eligible": False,
    }

    state_match = re.search(r"- State:\s*(.+)", content)
    if state_match:
        basics["state"] = state_match.group(1).strip()

    eligible_match = re.search(r"- Eligible:\s*(True|False)", content, re.IGNORECASE)
    if eligible_match:
        basics["eligible"] = eligible_match.group(1).lower() == "true"

    confidence_match = re.search(r"## Confidence Score\s*\n\s*(\d+)/100", content)
    if confidence_match:
        basics["confidence"] = int(confidence_match.group(1))

    return basics


def _list_report_files() -> list[Path]:
    if not REPORTS_DIR.exists():
        return []
    return sorted(REPORTS_DIR.glob("*.md"))


def _refined_cache_path(name: str) -> Path:
    return REFINED_DIR / f"{_report_filename(name)}.json"


def _load_refined_cache(name: str) -> dict | None:
    cache_path = _refined_cache_path(name)
    if not cache_path.exists():
        return None
    data = json.loads(cache_path.read_text(encoding="utf-8"))
    summary = data.get("executive_summary") or data.get("summary") or ""
    if summary.startswith("Unable to generate AI report"):
        cache_path.unlink(missing_ok=True)
        return None
    return data


def _save_refined_cache(name: str, data: dict) -> None:
    REFINED_DIR.mkdir(parents=True, exist_ok=True)
    _refined_cache_path(name).write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


class InstitutionService:
    def get_health(self) -> dict:
        return {"status": "ok"}

    def get_all_institutions(self) -> list[dict]:
        institutions = []

        for report_path in _list_report_files():
            content = report_path.read_text(encoding="utf-8")
            name = _extract_report_title(content) or report_path.stem.replace("_", " ")
            basics = _parse_report_basics(content)

            csv_row = _find_institution(name)
            if csv_row:
                institutions.append(
                    {
                        "name": name,
                        "state": csv_row["state"] or basics["state"],
                        "confidence": csv_row["confidence"] or basics["confidence"],
                        "eligible": csv_row["eligible"] if csv_row else basics["eligible"],
                    }
                )
            else:
                institutions.append(
                    {
                        "name": name,
                        "state": basics["state"],
                        "confidence": basics["confidence"],
                        "eligible": basics["eligible"],
                    }
                )

        if institutions:
            return institutions

        rows = _load_csv(QUALIFIED_CSV)
        return [
            {
                "name": row["name"],
                "state": row["state"],
                "confidence": row["confidence"],
                "eligible": row["eligible"],
            }
            for row in rows
        ]

    def get_institution(self, name: str, include_summary: bool = True) -> dict | None:
        report_path = REPORTS_DIR / f"{_report_filename(name)}.md"
        if not report_path.exists():
            profile = _find_institution(name)
            if not profile:
                return None
            profile["overview"] = ""
            profile["academic_strengths"] = ""
            profile["engineering_analysis"] = ""
            profile["management_analysis"] = ""
            profile["doctoral_analysis"] = ""
            profile["leadership_analysis"] = ""
            profile["confidence_assessment"] = ""
            profile["executive_summary"] = "Report not available for this institution."
            profile["summary"] = profile["executive_summary"]
            return profile

        cached = _load_refined_cache(name)
        if cached:
            cached["summary"] = cached.get("executive_summary", "")
            return cached

        report_content = report_path.read_text(encoding="utf-8")
        institution_name = _extract_report_title(report_content) or name

        try:
            refined = refine_report(report_content, institution_name)
            refined["summary"] = refined.get("executive_summary", "")
            _save_refined_cache(name, refined)
            return refined
        except Exception:
            refined = parse_report_locally(report_content, institution_name)
            refined["summary"] = refined.get("executive_summary", "")
            return refined

    def run_pipeline(self) -> dict:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            raise ValueError("SERPER_API_KEY environment variable is not set")

        target_qualified = int(os.getenv("TARGET_QUALIFIED", "20"))
        aishe_path = os.getenv(
            "AISHE_DATA_PATH",
            str(PROJECT_ROOT / "data" / "AISHE.xlsx"),
        )

        result = run_batch_pipeline(
            api_key=api_key,
            target_qualified=target_qualified,
            aishe_path=aishe_path,
        )

        if REFINED_DIR.exists():
            for cache_file in REFINED_DIR.glob("*.json"):
                cache_file.unlink()

        return result

    def get_report(self, name: str) -> dict | None:
        filepath = REPORTS_DIR / f"{_report_filename(name)}.md"
        if not filepath.exists():
            return None

        content = filepath.read_text(encoding="utf-8")
        return {
            "name": _extract_report_title(content) or name,
            "content": content,
        }
