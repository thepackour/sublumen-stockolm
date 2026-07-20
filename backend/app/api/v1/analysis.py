from fastapi import APIRouter

from app.schemas.analysis import AnalysisCreateRequest
from app.services.analysis_service import AnalysisService

router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["Analysis"]
)

service = AnalysisService()


@router.post("")
def create_analysis(request: AnalysisCreateRequest):
    return service.create_analysis(request)


@router.get("/{analysis_id}")
def get_analysis(analysis_id: str):
    return service.get_analysis(analysis_id)