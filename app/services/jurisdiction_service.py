class JurisdictionService:
    """Provide normalized summaries for jurisdiction guidance."""

    def summarize(self, data: dict) -> dict:
        if not data:
            return {
                "name": "Unknown jurisdiction",
                "overview": "No jurisdiction guidance is available for the selected region.",
                "frameworks": [],
                "data_residency": "No data residency guidance available.",
            }

        return {
            "name": data.get("name", "Unnamed jurisdiction"),
            "overview": data.get(
                "overview",
                "No jurisdiction overview is provided in the current library entry.",
            ),
            "frameworks": data.get("regulatory_frameworks", []),
            "data_residency": data.get(
                "data_residency",
                "No data residency guidance is configured for this jurisdiction.",
            ),
        }
