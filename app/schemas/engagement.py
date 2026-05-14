from pydantic import BaseModel, Field


class EngagementRequest(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=120)
    jurisdiction: str = Field(..., min_length=2, max_length=80)
    engagement_type: str = Field(..., min_length=2, max_length=80)
    target_type: str = Field(..., min_length=2, max_length=80)
    scope_text: str = Field(..., min_length=10, max_length=1200)
    cloud_provider: str = Field(..., min_length=2, max_length=80)

    class Config:
        anystr_strip_whitespace = True
        title = "Engagement request"
