import io
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime


def convert(zip_file: bytes) -> list[dict]:
    with zipfile.ZipFile(io.BytesIO(zip_file)) as z:
        xml_data = z.read("CORPCODE.xml")

    root = ET.fromstring(xml_data)
    return [
        {
            "corp_code": company.findtext("corp_code"),
            "corp_name": company.findtext("corp_name"),
            "corp_eng_name": company.findtext("corp_eng_name") or None,
            "stock_code": (company.findtext("stock_code") or "").strip() or None,
            "modify_date": datetime.strptime(
                company.findtext("modify_date"), "%Y%m%d"
            ).date(),
        }
        for company in root.findall("list")
    ]
