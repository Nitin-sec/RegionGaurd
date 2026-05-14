import re
from pathlib import Path


def ensure_directory_exists(path: Path) -> Path:
    """Create a directory if it does not already exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(value: str) -> str:
    """Create a Windows-safe filename fragment from freeform text."""
    normalized = re.sub(r"[^A-Za-z0-9 _-]", "", value).strip()
    normalized = re.sub(r"[-\s]+", "_", normalized)
    return normalized.lower() or "document"
