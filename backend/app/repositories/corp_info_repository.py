from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.schemas.corp_info import CorpInfo


class CorpInfoRepository:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save_all(self, corp_code_list: list[dict], batch_size: int = 5000) -> None:
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
        with self.session_factory() as db:
            for offset in range(0, len(corp_code_list), batch_size):
                stmt = insert(CorpInfo).values(
                    corp_code_list[offset:offset + batch_size]
                )
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
                db.execute(update_stmt)
            db.commit()

    def find_by_corp_code(self, corp_code: str) -> Optional[CorpInfo]:
        with self.session_factory() as db:
            return db.scalar(
                select(CorpInfo).where(CorpInfo.corp_code == corp_code)
            )

    def find_by_stock_code(self, stock_code: str) -> Optional[CorpInfo]:
        with self.session_factory() as db:
            return db.scalar(
                select(CorpInfo).where(CorpInfo.stock_code == stock_code)
            )

    def find_by_corp_name(
            self,
            corp_name: str,
    ) -> Optional[CorpInfo]:
        with self.session_factory() as db:
            return db.scalar(
                select(CorpInfo).where(CorpInfo.corp_name == corp_name)
            )

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

        with self.session_factory() as db:
            return list(db.scalars(stmt).all())

    def find_all_by_symbols(
            self,
            symbols: list[str],
    ) -> list[CorpInfo]:
        stmt = select(CorpInfo).where(CorpInfo.stock_code.in_(symbols))
        with self.session_factory() as db:
            return list(db.scalars(stmt).all())

    def find_all(self) -> list[CorpInfo]:
        with self.session_factory() as db:
            return list(db.scalars(select(CorpInfo)).all())
