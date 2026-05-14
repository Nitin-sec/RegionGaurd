import zipfile
from pathlib import Path

from ..utils.file_utils import ensure_directory_exists


class ExportService:
    """Package generated documents into a ZIP archive."""

    def __init__(self, output_dir: Path):
        self.output_dir = ensure_directory_exists(output_dir)

    def package_documents(self, file_paths: list[Path], package_name: str) -> Path:
        package_path = self.output_dir / package_name
        with zipfile.ZipFile(package_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for file_path in file_paths:
                archive.write(file_path, arcname=file_path.name)
        return package_path
