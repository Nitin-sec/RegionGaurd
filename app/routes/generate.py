from datetime import date

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse

from ..config import settings
from ..schemas.engagement import EngagementRequest
from ..services.docx_generator import DocxGenerator
from ..services.export_service import ExportService
from ..services.render_builder import RenderBuilder
from ..services.template_engine import TemplateEngine
from ..services.yaml_loader import YAMLLoader
from ..utils.file_utils import safe_filename

router = APIRouter()

yaml_loader = YAMLLoader(settings.library_root)
render_builder = RenderBuilder(yaml_loader)
template_engine = TemplateEngine(settings.templates_dir)
docx_generator = DocxGenerator(settings.docx_dir)
export_service = ExportService(settings.package_dir)


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

        date_stamp = date.today().strftime("%Y-%m-%d")
        client_key = safe_filename(client_name)
        base_name = f"{date_stamp}_{client_key}"

        generated_files = docx_generator.generate_all(render_data, base_name)
        package_file = export_service.package_documents(
            generated_files,
            f"{base_name}_package.zip",
        )

        download_files = [
            {"label": "Authorization letter", "name": generated_files[0].name},
            {"label": "Rules of engagement", "name": generated_files[1].name},
            {"label": "Scope definition", "name": generated_files[2].name},
        ]

        return template_engine.render(
            "html/result.html",
            {
                "render": render_data,
                "download_files": download_files,
                "package_file": package_file.name,
            },
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
