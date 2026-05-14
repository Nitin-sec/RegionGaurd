from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from ..config import settings

router = APIRouter()


def _build_safe_path(root: Path, file_name: str) -> Path:
    candidate = root / file_name
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")

    root_path = root.resolve()
    if root_path not in resolved.parents and resolved != root_path:
        raise HTTPException(status_code=400, detail="Invalid file path.")

    if not resolved.is_file():
        raise HTTPException(status_code=404, detail="File not found.")

    return resolved


@router.get("/download/docx/{file_name}", tags=["download"])
def download_docx(file_name: str):
    file_path = _build_safe_path(settings.docx_dir, file_name)
    return FileResponse(
        path=str(file_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=file_path.name,
    )


@router.get("/download/package/{file_name}", tags=["download"])
def download_package(file_name: str):
    file_path = _build_safe_path(settings.package_dir, file_name)
    return FileResponse(
        path=str(file_path),
        media_type="application/zip",
        filename=file_path.name,
    )
