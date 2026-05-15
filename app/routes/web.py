from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from ..config import settings
from ..services.template_engine import TemplateEngine
from ..services.yaml_loader import YAMLLoader

router = APIRouter()

yaml_loader = YAMLLoader(settings.library_root)
template_engine = TemplateEngine(settings.templates_dir)


@router.get("/", response_class=HTMLResponse, tags=["web"])
def home_page():
    """Render the landing page with option lists loaded from YAML assets."""
    yaml_loader.load_all()
    return template_engine.render(
        "html/index.html",
        {
            "jurisdictions": yaml_loader.list_jurisdictions(),
            "cloud_providers": yaml_loader.list_cloud_providers(),
            "engagement_presets": yaml_loader.list_engagement_presets(),
            "engagement_preset_data": yaml_loader._ensure_section("engagement_presets"),
        },
    )
