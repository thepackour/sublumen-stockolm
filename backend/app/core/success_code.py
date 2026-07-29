from enum import Enum

class SuccessCode(Enum):

    NEWS200_1 = (200, "NEWS200_1", "뉴스 조회에 성공했습니다.")
    NEWS200_2 = (200, "NEWS200_2", "뉴스 수집에 성공했습니다.")

    ANALYSIS200_1 = (200, "ANALYSIS200_1", "분석 조회에 성공했습니다.")
    ANALYSIS201_1 = (201, "ANALYSIS201_1", "분석 결과가 성공적으로 생성되었습니다.")

    STOCK200_1 = (200, "STOCK200_1", "종목 조회에 성공했습니다.")
    STOCK200_2 = (200, "STOCK200_2", "종목 상세 조회에 성공했습니다.")
    STOCK200_3 = (200, "STOCK200_3", "종목 차트 데이터 조회에 성공했습니다.")
    STOCK200_5 = (200, "STOCK200_5", "종목 과거 데이터 조회에 성공했습니다.")

    EXCHANGERATE200_1 = (200, "EXCHANGERATE200_1", "환율 조회에 성공했습니다.")

    @property
    def status(self):
        return self.value[0]
    
    @property
    def code(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]