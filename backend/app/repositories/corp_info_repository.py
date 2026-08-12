from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.schemas.corp_info import CorpInfo


class CorpInfoRepository:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save_all(self, corp_code_list: list[dict]):
        """
        모든 데이터 저장, 이미 저장된 데이터가 있으면 수정 일자가 갱신된 데이터만 수정

        Args:
            corp_code_list:

                - corp_code: 고유번호
                - corp_name: 정식명칭
                - corp_eng_name: 영문 정식명칭
                - stock_code: 종목코드 (symbol, ticker)
                - modify_date: 최종변경일자

        Returns: X

        """
        stmt = insert(CorpInfo).values([
            {
                "corp_code": c["corp_code"],
                "corp_name": c["corp_name"],
                "corp_eng_name": c["corp_eng_name"],
                "stock_code": c["stock_code"],
                "modify_date": c["modify_date"],
            }
            for c in corp_code_list
        ])

        update_stmt = stmt.on_conflict_do_update(
            index_elements=["corp_code"],
            set_={
                "corp_name": stmt.excluded.corp_name,
                "corp_eng_name": stmt.excluded.corp_eng_name,
                "stock_code": stmt.excluded.stock_code,
                "modify_date": stmt.excluded.modify_date,
            },
            where=(CorpInfo.modify_date < stmt.excluded.modify_date),
        )
        with self.session_factory() as db:
            db.execute(update_stmt)
            db.commit()

    def find_by_corp_name(
            self,
            corp_name: str,
    ) -> Optional[CorpInfo]:
        stmt = (
            select(CorpInfo)
            .where(CorpInfo.corp_name == corp_name)
        )
        return self.session_factory().execute(stmt)

    def search_by_keyword(
            self,
            keyword: str,
            limit: int | None = None,
    ) -> list[CorpInfo]:
        stmt = (
            select(CorpInfo)
            .where(
                CorpInfo.corp_name.ilike(f"%{keyword}%")
            )
        )

        if limit is not None:
            stmt = stmt.limit(limit)

        return list(self.session_factory().scalars(stmt).all())
