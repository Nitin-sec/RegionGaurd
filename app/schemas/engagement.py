from pydantic import BaseModel, Field, field_validator

_FIELD_HINTS = {
    "scope_assets": "Add at least one target — a URL, hostname, IP range, or cloud asset.",
    "objectives": "Describe at least one goal, e.g. 'Find authentication weaknesses'.",
    "exclusions": "List at least one exclusion, e.g. 'Payment processing' or 'Third-party APIs'.",
    "client_name": "Enter the client or organisation name.",
    "target_type": "Describe the target in one line, e.g. 'Customer web app on AWS'.",
}


class EngagementRequest(BaseModel):
    client_name: str = Field(..., max_length=120)
    jurisdiction: str = Field(..., max_length=80)
    engagement_preset: str = Field(..., max_length=80)
    target_type: str = Field(..., max_length=80)
    objectives: str = Field(..., max_length=1200)
    scope_assets: str = Field(..., max_length=1200)
    exclusions: str = Field(..., max_length=1200)
    testing_window: str = Field(default="To be confirmed", max_length=120)
    production_environment: bool = Field(default=False)
    authentication_provided: bool = Field(default=False)
    operational_notes: str = Field(default="", max_length=1200)
    cloud_provider: str = Field(..., max_length=80)

    model_config = {"str_strip_whitespace": True, "title": "Engagement request"}

    @field_validator("client_name", "target_type")
    @classmethod
    def require_nonempty_short(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(_FIELD_HINTS.get(info.field_name, "This field is required."))
        return v

    @field_validator("scope_assets", "objectives", "exclusions")
    @classmethod
    def require_nonempty_text(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(_FIELD_HINTS.get(info.field_name, "This field is required."))
        return v
