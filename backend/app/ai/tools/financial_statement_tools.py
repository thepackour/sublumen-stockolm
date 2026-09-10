from collections.abc import Callable

from langchain_core.tools import StructuredTool

from app.core.exceptions import ProjectException
from app.services.financial_statement_service import FinancialStatementService


class FinancialStatementTool:
    """Agent tools for investment-relevant OpenDART reports."""

    def __init__(self, financial_statement_service: FinancialStatementService):
        self.service = financial_statement_service

    def get_key_financial_accounts(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """매출, 영업이익, 순이익, 자산, 부채 등 주요 재무계정을 조회한다."""
        return self._call(self.service.get_key_financial_accounts, company, business_year, report_type)

    def get_financial_indicators(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """수익성, 안정성, 성장성, 활동성 재무지표를 조회한다."""
        return self._call(self.service.get_financial_indicators, company, business_year, report_type)

    def get_dividend_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """배당금과 배당수익률 등 배당 관련 정보를 조회한다."""
        return self._call(self.service.get_dividend_report, company, business_year, report_type)

    def get_treasury_stock_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """자기주식 취득 및 처분 현황을 조회한다."""
        return self._call(self.service.get_treasury_stock_report, company, business_year, report_type)

    def get_capital_change_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """증자와 감자 내역을 조회하여 주식 희석 또는 자본 감소 여부를 확인한다."""
        return self._call(self.service.get_capital_change_report, company, business_year, report_type)

    def get_share_count_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """발행 가능 주식, 발행주식, 자기주식, 유통주식 수를 조회한다."""
        return self._call(self.service.get_share_count_report, company, business_year, report_type)

    def get_audit_opinion_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """감사인, 감사의견, 강조사항과 핵심감사사항을 조회한다."""
        return self._call(self.service.get_audit_opinion_report, company, business_year, report_type)

    def get_major_shareholder_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """최대주주와 특수관계인의 보유 주식 및 지분율을 조회한다."""
        return self._call(self.service.get_major_shareholder_report, company, business_year, report_type)

    def get_minority_shareholder_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """소액주주 수와 보유 주식 비율을 조회한다."""
        return self._call(self.service.get_minority_shareholder_report, company, business_year, report_type)

    def get_other_corporate_investments(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        """다른 법인에 대한 출자 목적, 지분율과 장부가액을 조회한다."""
        return self._call(self.service.get_other_corporate_investments, company, business_year, report_type)

    @staticmethod
    def _call(method: Callable, company: str, business_year: int | None, report_type: str) -> dict:
        try:
            return method(company, business_year, report_type)
        except ProjectException as exc:
            return {
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                }
            }

    def get_tools(self) -> list[StructuredTool]:
        common = (
            " company에는 회사명, 6자리 종목코드 또는 8자리 DART 고유번호를 입력한다."
            " business_year를 생략하면 직전 연도를 사용한다."
            " report_type은 annual, half, q1, q3 중 하나다."
        )
        definitions = [
            (self.get_key_financial_accounts, "dart_key_financial_accounts", "주요 재무계정을 조회한다."),
            (self.get_financial_indicators, "dart_financial_indicators", "수익성·안정성·성장성·활동성 지표를 조회한다."),
            (self.get_dividend_report, "dart_dividend_report", "배당 및 주주환원 정보를 조회한다."),
            (self.get_treasury_stock_report, "dart_treasury_stock_report", "자기주식 취득·처분 현황을 조회한다."),
            (self.get_capital_change_report, "dart_capital_change_report", "증자·감자와 희석 위험을 조회한다."),
            (self.get_share_count_report, "dart_share_count_report", "발행·자기·유통주식 수를 조회한다."),
            (self.get_audit_opinion_report, "dart_audit_opinion_report", "감사의견과 핵심감사사항을 조회한다."),
            (self.get_major_shareholder_report, "dart_major_shareholder_report", "최대주주 지분 현황을 조회한다."),
            (self.get_minority_shareholder_report, "dart_minority_shareholder_report", "소액주주 현황을 조회한다."),
            (self.get_other_corporate_investments, "dart_other_corporate_investments", "타법인 출자와 자본배분 현황을 조회한다."),
        ]
        return [
            StructuredTool.from_function(
                func=method,
                name=name,
                description=description + common,
            )
            for method, name, description in definitions
        ]
