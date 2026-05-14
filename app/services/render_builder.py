from .jurisdiction_service import JurisdictionService
from .yaml_loader import YAMLLoader
from ..schemas.engagement import EngagementRequest


class RenderBuilder:
    """Flatten engagement inputs and library content into a render payload."""

    def __init__(self, yaml_loader: YAMLLoader, jurisdiction_service: JurisdictionService | None = None):
        self.yaml_loader = yaml_loader
        self.jurisdiction_service = jurisdiction_service or JurisdictionService()

    def build_render_data(self, engagement: EngagementRequest) -> dict:
        jurisdiction_data = self.yaml_loader.get_jurisdiction(engagement.jurisdiction)
        cloud_data = self.yaml_loader.get_cloud_provider(engagement.cloud_provider)
        roe_data = self.yaml_loader.get_roe_preset(engagement.engagement_type)

        if not jurisdiction_data:
            raise ValueError(f"Jurisdiction data not found for '{engagement.jurisdiction}'.")
        if not cloud_data:
            raise ValueError(f"Cloud provider data not found for '{engagement.cloud_provider}'.")
        if not roe_data:
            raise ValueError(f"Rules of engagement preset not found for '{engagement.engagement_type}'.")

        jurisdiction_summary = self.jurisdiction_service.summarize(jurisdiction_data)

        return {
            "client_name": engagement.client_name,
            "target_type": engagement.target_type,
            "scope_text": engagement.scope_text,
            "jurisdiction_key": engagement.jurisdiction,
            "jurisdiction_name": jurisdiction_summary["name"],
            "jurisdiction_overview": jurisdiction_summary["overview"],
            "jurisdiction_frameworks": jurisdiction_summary["frameworks"],
            "jurisdiction_data_residency": jurisdiction_summary["data_residency"],
            "cloud_provider_key": engagement.cloud_provider,
            "cloud_provider_name": cloud_data.get("name", engagement.cloud_provider),
            "cloud_provider_summary": cloud_data.get(
                "summary",
                "No cloud provider summary is available for the selected asset.",
            ),
            "cloud_provider_controls": cloud_data.get("security_controls", []),
            "cloud_provider_region_coverage": cloud_data.get("region_coverage", []),
            "roe_preset_key": engagement.engagement_type,
            "roe_preset_name": roe_data.get("name", engagement.engagement_type),
            "roe_description": roe_data.get(
                "description",
                "No rules of engagement description is available.",
            ),
            "roe_guidance": roe_data.get("rules_of_engagement", []),
            "roe_scope_limitations": roe_data.get("scope_limitations", ""),
            "roe_report_timing": roe_data.get("report_timing", ""),
        }
