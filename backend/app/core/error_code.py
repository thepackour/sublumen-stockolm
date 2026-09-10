from enum import Enum

class ErrorCode(Enum):

    NEWS400_1 = (400, "NEWS400_1", "API 호출 중 클라이언트 측 오류가 발생했습니다.")
    NEWS404_1 = (404, "NEWS404_1", "뉴스를 찾을 수 없습니다.")
    NEWS500_1 = (500, "NEWS500_1", "뉴스 조회 API 호출에 실패했습니다.")

    ANALYSIS404_1 = (404, "ANALYSIS404_1", "분석을 찾을 수 없습니다.")
    ANALYSIS400_1 = (400, "ANALYSIS400_1", "분석 요청이 유효하지 않습니다.")

    TECHNICAL_ANALYSIS400_1 = (400, "TECHNICAL_ANALYSIS400_1", "기술적 분석 요청 또는 전략 파라미터가 유효하지 않습니다.")
    TECHNICAL_ANALYSIS400_2 = (400, "TECHNICAL_ANALYSIS400_2", "기술 지표를 계산하기 위한 주가 데이터가 부족합니다.")

    STOCK400_1 = (400, "STOCK400_1", "종목 요청이 유효하지 않습니다.")
    STOCK404_1 = (404, "STOCK404_1", "종목을 찾을 수 없습니다.")

    EXCHANGERATE404_1 = (404, "EXCHANGERATE404_1", "환율 정보를 찾을 수 없습니다.")

    BACKTEST404_1 = (404, "BACKTEST404_1", "백테스트 결과를 찾을 수 없습니다.")
    BACKTEST400_1 = (400, "BACKTEST400_1", "백테스트 요청이 유효하지 않습니다.")

    FS400_1 = (400, "FS400_1", "end_year와 end_quarter는 함께 지정해야 합니다.")
    FS400_2 = (400, "FS400_2", "시작 일자는 2015년 이후여야 합니다.")
    FS400_3 = (400, "FS400_3", "시작 일자는 현재 이전 분기여야 합니다.")
    FS400_4 = (400, "FS400_4", "끝 일자는 2015년 이후여야 합니다.")
    FS400_5 = (400, "FS400_5", "끝 일자는 현재 이전 분기여야 합니다.")
    FS400_6 = (400, "FS400_6", "끝 일자는 시작 일자 이후여야 합니다.")
    FS400_7 = (400, "FS400_7", "보고서 유형이 올바르지 않습니다.")
    FS400_8 = (400, "FS400_8", "사업연도는 2015년부터 현재 연도까지 지정할 수 있습니다.")
    FS404_1 = (404, "FS404_1", "DART 기업 정보를 찾을 수 없습니다.")

    DART400_1 = (400, "DART400_1", "OpenDART 요청 값이 올바르지 않습니다.")
    DART401_1 = (401, "DART401_1", "OpenDART 인증키를 확인해 주세요.")
    DART429_1 = (429, "DART429_1", "OpenDART 요청 한도를 초과했습니다.")
    DART500_1 = (503, "DART500_1", "OpenDART 서비스를 이용할 수 없습니다.")

    GENERAL400_1 = (400, "GENERAL400_1", "잘못된 요청입니다.")
    GENERAL401_1 = (401, "GENERAL401_1", "인증되지 않은 요청입니다.")
    GENERAL403_1 = (403, "GENERAL403_1", "권한이 없는 요청입니다.")
    GENERAL404_1 = (404, "GENERAL404_1", "요청한 리소스를 찾을 수 없습니다.")
    GENERAL500_1 = (500, "GENERAL500_1", "서버 내부 오류가 발생했습니다.")

    @property
    def status(self):
        return self.value[0]
    
    @property
    def code(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]
