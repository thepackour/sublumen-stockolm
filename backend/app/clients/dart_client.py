from __future__ import annotations

from typing import Any

import requests

from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.util.zip_converter import convert


class DartClient:
    """Small client for the OpenDART endpoints used by the investment agent."""

    def __init__(
            self,
            api_key: str,
            base_url: str = "https://opendart.fss.or.kr/api",
            timeout_seconds: float = 10.0,
            http_client=requests,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.http_client = http_client

    def get_report(
            self,
            endpoint: str,
            corp_code: str,
            business_year: int,
            report_code: str,
            **extra_params: str,
    ) -> list[dict[str, Any]]:
        data = self._get_json(
            endpoint,
            {
                "corp_code": corp_code,
                "bsns_year": str(business_year),
                "reprt_code": report_code,
                **extra_params,
            },
        )
        return data.get("list") or []

    def get_corp_codes(self) -> list[dict]:
        self._require_api_key()
        try:
            response = self.http_client.get(
                f"{self.base_url}/corpCode.xml",
                params={"crtfc_key": self.api_key},
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            return convert(response.content)
        except Exception as exc:
            raise ProjectException(ErrorCode.DART500_1) from exc

    def _get_json(self, endpoint: str, params: dict[str, str]) -> dict[str, Any]:
        self._require_api_key()
        try:
            response = self.http_client.get(
                f"{self.base_url}/{endpoint}",
                params={"crtfc_key": self.api_key, **params},
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise ProjectException(ErrorCode.DART500_1) from exc

        status = data.get("status")
        if status in (None, "000"):
            return data
        if status == "013":
            return {"status": status, "message": data.get("message"), "list": []}
        if status in {"010", "011", "012", "901"}:
            raise ProjectException(ErrorCode.DART401_1)
        if status == "020":
            raise ProjectException(ErrorCode.DART429_1)
        if status in {"021", "100", "101"}:
            raise ProjectException(ErrorCode.DART400_1)
        raise ProjectException(ErrorCode.DART500_1)

    def _require_api_key(self) -> None:
        if not self.api_key:
            raise ProjectException(ErrorCode.DART401_1)
