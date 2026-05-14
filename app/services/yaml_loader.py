from pathlib import Path

import yaml
from yaml import YAMLError


class YAMLLoader:
    """Load local YAML libraries and expose them through simple helpers."""

    def __init__(self, library_root: Path):
        self.library_root = library_root
        self._cache = {
            "jurisdictions": None,
            "cloud_providers": None,
            "roe_presets": None,
        }

    def _load_folder(self, folder_name: str) -> dict:
        folder_path = self.library_root / folder_name
        if not folder_path.exists():
            return {}

        collection = {}
        for yaml_file in sorted(folder_path.glob("*.yaml")):
            try:
                content = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or {}
                collection[yaml_file.stem] = content
            except (YAMLError, OSError) as exc:
                # Fail safely and keep loading remaining files
                collection[yaml_file.stem] = {
                    "name": yaml_file.stem,
                    "error": f"Unable to load YAML: {exc}",
                }
        return collection

    def _ensure_section(self, section: str) -> dict:
        if self._cache.get(section) is None:
            self._cache[section] = self._load_folder(section)
        return self._cache[section]

    def load_all(self) -> None:
        """Load all supported library folders into memory."""
        for section in self._cache:
            self._cache[section] = self._load_folder(section)

    def list_jurisdictions(self) -> list[dict[str, str]]:
        collection = self._ensure_section("jurisdictions")
        return [
            {"key": key, "label": data.get("name", key)}
            for key, data in sorted(collection.items(), key=lambda item: item[1].get("name", item[0]))
        ]

    def list_cloud_providers(self) -> list[dict[str, str]]:
        collection = self._ensure_section("cloud_providers")
        return [
            {"key": key, "label": data.get("name", key)}
            for key, data in sorted(collection.items(), key=lambda item: item[1].get("name", item[0]))
        ]

    def list_roe_presets(self) -> list[dict[str, str]]:
        collection = self._ensure_section("roe_presets")
        return [
            {"key": key, "label": data.get("name", key)}
            for key, data in sorted(collection.items(), key=lambda item: item[1].get("name", item[0]))
        ]

    def get_jurisdiction(self, key: str) -> dict:
        return self._ensure_section("jurisdictions").get(key, {})

    def get_cloud_provider(self, key: str) -> dict:
        return self._ensure_section("cloud_providers").get(key, {})

    def get_roe_preset(self, key: str) -> dict:
        return self._ensure_section("roe_presets").get(key, {})
