import io
import zipfile

import pytest

from app.clients.dart_client import DartClient
from app.core.exceptions import ProjectException


class FakeResponse:
    def __init__(self, data=None, content=b""):
        self._data = data
        self.content = content

    def raise_for_status(self):
        return None

    def json(self):
        return self._data


class FakeHttpClient:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def get(self, url, params, timeout):
        self.calls.append((url, params, timeout))
        return self.response


def test_report_request_uses_open_dart_parameter_names():
    http = FakeHttpClient(FakeResponse({"status": "000", "list": [{"x": 1}]}))
    client = DartClient("key", "https://dart.test/api", 3, http)

    result = client.get_report(
        "fnlttSinglIndx.json",
        "00126380",
        2025,
        "11011",
        idx_cl_code="M210000",
    )

    assert result == [{"x": 1}]
    assert http.calls == [(
        "https://dart.test/api/fnlttSinglIndx.json",
        {
            "crtfc_key": "key",
            "corp_code": "00126380",
            "bsns_year": "2025",
            "reprt_code": "11011",
            "idx_cl_code": "M210000",
        },
        3,
    )]


def test_no_data_status_is_an_empty_result():
    http = FakeHttpClient(FakeResponse({"status": "013", "message": "no data"}))
    client = DartClient("key", http_client=http)

    assert client.get_report("alotMatter.json", "00126380", 2025, "11011") == []


def test_missing_api_key_is_reported_before_an_http_call():
    http = FakeHttpClient(FakeResponse())
    client = DartClient("", http_client=http)

    with pytest.raises(ProjectException) as exc_info:
        client.get_report("alotMatter.json", "00126380", 2025, "11011")

    assert exc_info.value.code == "DART401_1"
    assert http.calls == []


def test_corp_code_zip_is_converted_to_company_records():
    xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <result><list><corp_code>00126380</corp_code><corp_name>Samsung</corp_name>
    <corp_eng_name>Samsung Electronics</corp_eng_name><stock_code>005930</stock_code>
    <modify_date>20260101</modify_date></list></result>"""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("CORPCODE.xml", xml)

    http = FakeHttpClient(FakeResponse(content=buffer.getvalue()))
    client = DartClient("key", http_client=http)

    result = client.get_corp_codes()

    assert result[0]["corp_code"] == "00126380"
    assert result[0]["stock_code"] == "005930"
    assert result[0]["modify_date"].isoformat() == "2026-01-01"
