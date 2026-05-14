from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_root: Path = Path(__file__).resolve().parents[1]
    templates_dir: Path = project_root / "app" / "templates"
    static_dir: Path = project_root / "app" / "static"
    library_root: Path = project_root / "app" / "library"
    generated_dir: Path = project_root / "generated"
    docx_dir: Path = generated_dir / "docx"
    package_dir: Path = generated_dir / "packages"


settings = Settings()
