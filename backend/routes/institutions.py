from fastapi import APIRouter, HTTPException

from backend.models.response_models import (
    HealthResponse,
    InstitutionDetailResponse,
    InstitutionSummary,
    PipelineRunResponse,
    ReportResponse,
)
from backend.services.institution_service import InstitutionService

router = APIRouter()
service = InstitutionService()


@router.get("/health", response_model=HealthResponse)
def health_check():
    return service.get_health()


@router.get("/institutions", response_model=list[InstitutionSummary])
def list_institutions():
    return service.get_all_institutions()


@router.get("/institutions/{name}", response_model=InstitutionDetailResponse)
def get_institution(name: str):
    profile = service.get_institution(name)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Institution not found: {name}")
    return profile


@router.post("/run-pipeline", response_model=PipelineRunResponse)
def run_pipeline():
    try:
        return service.run_pipeline()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline execution failed: {exc}",
        ) from exc


@router.get("/reports/{name}", response_model=ReportResponse)
def get_report(name: str):
    report = service.get_report(name)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report not found: {name}")
    return report
