from pydantic import BaseModel, Field


class EngagementRequest(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=120)
    jurisdiction: str = Field(..., min_length=2, max_length=80)
    engagement_preset: str = Field(..., min_length=2, max_length=80)
    target_type: str = Field(..., min_length=2, max_length=80)
    objectives: str = Field(..., min_length=10, max_length=1200)
    scope_assets: str = Field(..., min_length=10, max_length=1200)
    exclusions: str = Field(..., min_length=10, max_length=1200)
    testing_window: str = Field(default="To be confirmed", max_length=120)
    production_environment: bool = Field(...)
    authentication_provided: bool = Field(...)
    operational_notes: str = Field(default="", max_length=1200)
    cloud_provider: str = Field(..., min_length=2, max_length=80)

    class Config:
        anystr_strip_whitespace = True
        title = "Engagement request"
