from fastapi import APIRouter
from fastapi.responses import FileResponse

from main import run_pipeline
from src.export.excel_export import export_to_excel

router = APIRouter(prefix="/catalogue", tags=["Catalogue"])

@router.post("/generate")
def generate_catalogue():
    results = run_pipeline()
    output_path = export_to_excel(results)

    return FileResponse(
        path = output_path,
        filename="content_metadata_catalogue.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )