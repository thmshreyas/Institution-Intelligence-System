import json
import os
import time

from google import genai
from google.genai import types

from src.llm.report_parser import parse_report_locally

REFINED_REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "state": {"type": "string"},
        "website": {"type": "string"},
        "established_year": {"type": "integer"},
        "age": {"type": "integer"},
        "engineering": {"type": "boolean"},
        "mba": {"type": "boolean"},
        "phd": {"type": "boolean"},
        "eligible": {"type": "boolean"},
        "vice_chancellor": {"type": "string"},
        "address": {"type": "string"},
        "confidence": {"type": "integer"},
        "overview": {"type": "string"},
        "academic_strengths": {"type": "string"},
        "engineering_analysis": {"type": "string"},
        "management_analysis": {"type": "string"},
        "doctoral_analysis": {"type": "string"},
        "leadership_analysis": {"type": "string"},
        "confidence_assessment": {"type": "string"},
        "executive_summary": {"type": "string"},
    },
    "required": [
        "name",
        "overview",
        "academic_strengths",
        "engineering_analysis",
        "management_analysis",
        "doctoral_analysis",
        "leadership_analysis",
        "confidence_assessment",
        "executive_summary",
    ],
}


def _use_gemini() -> bool:
    return os.getenv("USE_GEMINI", "true").strip().lower() in {"1", "true", "yes"}


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    return genai.Client(api_key=api_key)


def _is_quota_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "429" in message or "resource_exhausted" in message or "quota" in message


def _refine_with_gemini(report_content: str, institution_name: str) -> dict:
    client = _get_client()
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    prompt = f"""You are an institutional intelligence analyst. Read the markdown institution report below and produce refined structured intelligence data.

Extract all factual fields from the report. Then write professional analysis sections based only on the provided data.

Institution: {institution_name}

Report:
{report_content}

Return JSON with these fields:
- name, state, website, established_year, age
- engineering, mba, phd, eligible (booleans)
- vice_chancellor, address, confidence (0-100 integer)
- overview: 1 paragraph institution overview
- academic_strengths: 1 paragraph on academic strengths and maturity
- engineering_analysis: brief analysis of engineering presence
- management_analysis: brief analysis of MBA/management presence
- doctoral_analysis: brief analysis of PhD/doctoral presence
- leadership_analysis: brief analysis of leadership information
- confidence_assessment: brief assessment of the confidence score
- executive_summary: 2-3 sentence executive summary

Do not invent facts beyond the report. Use null for missing numeric fields and empty strings for missing text."""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=REFINED_REPORT_SCHEMA,
        ),
    )

    data = json.loads(response.text)
    data["name"] = data.get("name") or institution_name
    data["generated_by"] = "gemini"
    return data


def refine_report(report_content: str, institution_name: str) -> dict:
    if not _use_gemini():
        return parse_report_locally(report_content, institution_name)

    try:
        return _refine_with_gemini(report_content, institution_name)
    except Exception as exc:
        if _is_quota_error(exc):
            time.sleep(1)
        return parse_report_locally(report_content, institution_name)
