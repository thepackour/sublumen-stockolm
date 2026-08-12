import io
import zipfile
import xml.etree.ElementTree as ET


def convert(zip_file: bytes) -> list[dict]:
    with zipfile.ZipFile(io.BytesIO(zip_file)) as z:
        xml_data = z.read("CORPCODE.xml")

    root = ET.fromstring(xml_data)
    return [
        {
            "corp_code": company.findtext("corp_code"),
            "corp_name": company.findtext("corp_name"),
            "stock_code": company.findtext("stock_code").strip(),  # 상장사는 6자리, 비상장사는 빈값/공백
            "modify_date": company.findtext("modify_date"),
        }
        for company in root.findall("list")
    ]