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
        preset_data = self.yaml_loader.get_engagement_preset(engagement.engagement_preset)

        if not jurisdiction_data:
            raise ValueError(f"Jurisdiction data not found for '{engagement.jurisdiction}'.")
        if not cloud_data:
            raise ValueError(f"Cloud provider data not found for '{engagement.cloud_provider}'.")
        if not preset_data:
            raise ValueError(f"Engagement preset not found for '{engagement.engagement_preset}'.")

        jurisdiction_summary = self.jurisdiction_service.summarize(jurisdiction_data)
        scope_items = self._normalize_list(engagement.scope_assets)
        objective_items = self._normalize_list(engagement.objectives)
        exclusion_items = self._normalize_list(engagement.exclusions)

        return {
            "client_name": engagement.client_name,
            "target_type": engagement.target_type,
            "engagement_preset_key": engagement.engagement_preset,
            "engagement_preset_name": preset_data.get("display_name", engagement.engagement_preset),
            "engagement_preset_description": preset_data.get("description", ""),
            "preset_scope_examples": preset_data.get("suggested_scope_examples", []),
            "preset_roe_notes": preset_data.get("recommended_roe_notes", []),
            "preset_testing_window": preset_data.get("recommended_testing_window", ""),
            "preset_operational_considerations": preset_data.get("operational_considerations", []),
            "objectives_text": engagement.objectives,
            "objectives_list": objective_items,
            "scope_text": engagement.scope_assets,
            "scope_assets_list": scope_items,
            "exclusions_text": engagement.exclusions,
            "exclusions_list": exclusion_items,
            "testing_window": engagement.testing_window,
            "production_environment": engagement.production_environment,
            "authentication_provided": engagement.authentication_provided,
            "operational_notes": engagement.operational_notes,
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
        }

    def _normalize_list(self, text: str) -> list[str]:
        return [line.strip() for line in text.splitlines() if line.strip()]
