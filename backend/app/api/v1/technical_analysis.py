from fastapi import APIRouter, Depends

from app.container import container
from app.schemas.technical_analysis import TechnicalAnalysisRequest
from app.services.technical_analysis_service import TechnicalAnalysisService


router = APIRouter(
    prefix="/api/v1/technical-analysis",
    tags=["Technical Analysis"],
)


def get_technical_analysis_service() -> TechnicalAnalysisService:
    return container.technical_analysis_service


@router.get("/strategies")
def get_strategies(
    service: TechnicalAnalysisService = Depends(get_technical_analysis_service),
):
    return service.available_strategies()


@router.post("")
def create_technical_analysis(
    request: TechnicalAnalysisRequest,
    service: TechnicalAnalysisService = Depends(get_technical_analysis_service),
):
    return service.analyze(
        symbol=request.symbol,
        strategy_name=request.strategy,
        start_date=request.start_date,
        end_date=request.end_date,
        parameters=request.parameters,
        include_history=request.include_history,
    )
