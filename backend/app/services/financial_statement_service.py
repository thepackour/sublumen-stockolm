from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from threading import Lock

from app.clients.dart_client import DartClient
from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.repositories.corp_info_repository import CorpInfoRepository


REPORT_CODES = {
    "annual": "11011",
    "half": "11012",
    "q1": "11013",
    "q3": "11014",
}

REPORT_TYPE_ALIASES = {
    "annual": "annual",
    "year": "annual",
    "사업": "annual",
    "사업보고서": "annual",
    "half": "half",
    "half_year": "half",
    "반기": "half",
    "반기보고서": "half",
    "q1": "q1",
    "1q": "q1",
    "1분기": "q1",
    "1분기보고서": "q1",
    "q3": "q3",
    "3q": "q3",
    "3분기": "q3",
    "3분기보고서": "q3",
}

INDICATOR_CATEGORIES = {
    "profitability": "M210000",
    "stability": "M220000",
    "growth": "M230000",
    "activity": "M240000",
}


@dataclass(frozen=True)
class ResolvedCompany:
    corp_code: str
    corp_name: str | None = None
    stock_code: str | None = None


class FinancialStatementService:
    """Queries a focused set of OpenDART reports useful for investing."""

    def __init__(
            self,
            dart_client: DartClient,
            corp_info_repository: CorpInfoRepository,
            max_items: int = 50,
    ):
        self.dart_client = dart_client
        self.corp_info_repository = corp_info_repository
        self.max_items = max_items
        self._catalog_refresh_attempted = False
        self._catalog_lock = Lock()

    def get_key_financial_accounts(
            self,
            company: str,
            business_year: int | None = None,
            report_type: str = "annual",
    ) -> dict:
        return self._query(
            "key_financial_accounts",
            "fnlttSinglAcnt.json",
            company,
            business_year,
            report_type,
        )

    def get_financial_indicators(
            self,
            company: str,
            business_year: int | None = None,
            report_type: str = "annual",
    ) -> dict:
        resolved, year, normalized_report_type, report_code = self._context(
            company, business_year, report_type
        )
        items = []
        for category, category_code in INDICATOR_CATEGORIES.items():
            category_items = self.dart_client.get_report(
                "fnlttSinglIndx.json",
                resolved.corp_code,
                year,
                report_code,
                idx_cl_code=category_code,
            )
            items.extend(
                {"indicator_category": category, **item}
                for item in category_items
            )
        return self._result(
            "financial_indicators",
            resolved,
            year,
            normalized_report_type,
            items,
        )

    def get_dividend_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        return self._query("dividends", "alotMatter.json", company, business_year, report_type)

    def get_treasury_stock_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        return self._query("treasury_stock", "tesstkAcqsDspsSttus.json", company, business_year, report_type)

    def get_capital_change_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        return self._query("capital_changes", "irdsSttus.json", company, business_year, report_type)

    def get_share_count_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        return self._query("share_count", "stockTotqySttus.json", company, business_year, report_type)

    def get_audit_opinion_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        return self._query("audit_opinion", "accnutAdtorNmNdAdtOpinion.json", company, business_year, report_type)

    def get_major_shareholder_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        return self._query("major_shareholder", "hyslrSttus.json", company, business_year, report_type)

    def get_minority_shareholder_report(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        return self._query("minority_shareholder", "mrhlSttus.json", company, business_year, report_type)

    def get_other_corporate_investments(self, company: str, business_year: int | None = None, report_type: str = "annual") -> dict:
        return self._query("other_corporate_investments", "otrCprInvstmntSttus.json", company, business_year, report_type)

    def _query(
            self,
            report_name: str,
            endpoint: str,
            company: str,
            business_year: int | None,
            report_type: str,
    ) -> dict:
        resolved, year, normalized_report_type, report_code = self._context(
            company, business_year, report_type
        )
        items = self.dart_client.get_report(
            endpoint,
            resolved.corp_code,
            year,
            report_code,
        )
        return self._result(
            report_name,
            resolved,
            year,
            normalized_report_type,
            items,
        )

    def _context(
            self,
            company: str,
            business_year: int | None,
            report_type: str,
    ) -> tuple[ResolvedCompany, int, str, str]:
        normalized_report_type = REPORT_TYPE_ALIASES.get(report_type.strip().lower())
        if normalized_report_type is None:
            raise ProjectException(ErrorCode.FS400_7)

        year = business_year or date.today().year - 1
        if year < 2015 or year > date.today().year:
            raise ProjectException(ErrorCode.FS400_8)

        resolved = self._resolve_company(company)
        return (
            resolved,
            year,
            normalized_report_type,
            REPORT_CODES[normalized_report_type],
        )

    def _resolve_company(self, company: str) -> ResolvedCompany:
        query = company.strip()
        if not query:
            raise ProjectException(ErrorCode.FS404_1)

        if query.isdigit() and len(query) == 8:
            corp = self.corp_info_repository.find_by_corp_code(query)
            return self._resolved(corp) if corp else ResolvedCompany(query)

        corp = self._find_company(query)
        if corp is None:
            self._refresh_corp_catalog_once()
            corp = self._find_company(query)
        if corp is None:
            raise ProjectException(ErrorCode.FS404_1)
        return self._resolved(corp)

    def _find_company(self, query: str):
        if query.isdigit() and len(query) == 6:
            return self.corp_info_repository.find_by_stock_code(query)

        exact = self.corp_info_repository.find_by_corp_name(query)
        if exact is not None:
            return exact

        matches = self.corp_info_repository.search_by_keyword(query, limit=10)
        if not matches:
            return None
        return min(matches, key=lambda corp: len(corp.corp_name))

    def _refresh_corp_catalog_once(self) -> None:
        if self._catalog_refresh_attempted:
            return
        with self._catalog_lock:
            if self._catalog_refresh_attempted:
                return
            corp_codes = self.dart_client.get_corp_codes()
            self.corp_info_repository.save_all(corp_codes)
            self._catalog_refresh_attempted = True

    @staticmethod
    def _resolved(corp) -> ResolvedCompany:
        return ResolvedCompany(
            corp_code=corp.corp_code,
            corp_name=corp.corp_name,
            stock_code=corp.stock_code,
        )

    def _result(
            self,
            report_name: str,
            company: ResolvedCompany,
            business_year: int,
            report_type: str,
            items: list[dict],
    ) -> dict:
        visible_items = items[:self.max_items]
        return {
            "report": report_name,
            "company": asdict(company),
            "business_year": business_year,
            "report_type": report_type,
            "item_count": len(items),
            "truncated": len(items) > len(visible_items),
            "items": visible_items,
        }
