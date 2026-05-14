from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse

from ..config import settings
from ..schemas.engagement import EngagementRequest
from ..services.render_builder import RenderBuilder
from ..services.template_engine import TemplateEngine
from ..services.yaml_loader import YAMLLoader

router = APIRouter()

yaml_loader = YAMLLoader(settings.library_root)
render_builder = RenderBuilder(yaml_loader)
template_engine = TemplateEngine(settings.templates_dir)


@router.post("/generate", response_class=HTMLResponse, tags=["generate"])
def generate_summary(
    client_name: str = Form(...),
    jurisdiction: str = Form(...),
    engagement_type: str = Form(...),
    target_type: str = Form(...),
    scope_text: str = Form(...),
    cloud_provider: str = Form(...),
):
    """Build and render a deterministic engagement briefing page from form inputs."""
    try:
        request_data = EngagementRequest(
            client_name=client_name,
            jurisdiction=jurisdiction,
            engagement_type=engagement_type,
            target_type=target_type,
            scope_text=scope_text,
            cloud_provider=cloud_provider,
        )
        render_data = render_builder.build_render_data(request_data)
        return template_engine.render("html/result.html", {"render": render_data})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
