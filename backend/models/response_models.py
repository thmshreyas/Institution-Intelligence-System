from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class InstitutionSummary(BaseModel):
    name: str
    state: str | None = None
    confidence: int = 0
    eligible: bool = False


class InstitutionProfile(BaseModel):
    name: str
    state: str | None = None
    website: str | None = None
    established_year: int | None = None
    age: int | None = None
    engineering: bool = False
    mba: bool = False
    phd: bool = False
    vice_chancellor: str | None = None
    address: str | None = None
    confidence: int = 0
    eligible: bool = False


class InstitutionDetailResponse(InstitutionProfile):
    overview: str = ""
    academic_strengths: str = ""
    engineering_analysis: str = ""
    management_analysis: str = ""
    doctoral_analysis: str = ""
    leadership_analysis: str = ""
    confidence_assessment: str = ""
    executive_summary: str = Field(
        default="",
        description="AI-generated executive summary",
    )
    summary: str = Field(
        default="",
        description="Alias for executive_summary (backward compatible)",
    )


class PipelineRunResponse(BaseModel):
    status: str
    qualified_count: int


class ReportResponse(BaseModel):
    name: str
    content: str
