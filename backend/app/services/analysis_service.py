from app.core.exceptions import ProjectException
from app.core.error_code import ErrorCode
from app.repositories.mock_stock_repository import StockRepository
from app.schemas.analysis import AnalysisCreateRequest

stock_repository = StockRepository()


class AnalysisService:

    def __init__(self):
        self.analysis_store: dict[str, dict] = {}

    def create_analysis(self, request):

        # 뉴스 조회
        news = ...

        # 재무정보 조회
        financial = ...

        # GPT 호출
        result = ...

        # 저장
        ...

        return result
    
    
    def create_analysis(self, request: AnalysisCreateRequest):
        analysis_id = f"analysis-{len(self.analysis_store) + 1}"
        detail = stock_repository.get_stock_detail(request.symbol)
        self.analysis_store[analysis_id] = {
            "analysisId": analysis_id,
            "symbol": detail["symbol"],
            "analysisType": request.analysis_type,
            "summary": f"{detail['name']}는 {detail['sector']} 업종에서 안정적인 흐름을 보이고 있습니다.",
            "riskLevel": "중간",
            "score": 74,
        }
        return self.analysis_store[analysis_id]



    def get_analysis(self, analysis_id: str):
        if analysis_id not in self.analysis_store:
            raise ProjectException(ErrorCode.ANALYSIS404_1)
        return self.analysis_store[analysis_id]