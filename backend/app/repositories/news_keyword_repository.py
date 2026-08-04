from datetime import datetime

from sqlalchemy import select, update

from app.schemas.news_keyword import NewsKeyword

now = datetime.now()

keywords = [
    NewsKeyword(
        keyword="삼성전자",
        priority=10,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="SK하이닉스",
        priority=10,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="현대차",
        priority=8,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="기아",
        priority=8,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="LG에너지솔루션",
        priority=8,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="NAVER",
        priority=7,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="카카오",
        priority=6,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="한화오션",
        priority=7,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="두산에너빌리티",
        priority=7,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="포스코홀딩스",
        priority=6,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="엔비디아",
        priority=10,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="애플",
        priority=8,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="테슬라",
        priority=9,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="마이크로소프트",
        priority=7,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="AI 반도체",
        priority=9,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="2차전지",
        priority=8,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="반도체",
        priority=10,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="원전",
        priority=6,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="방산",
        priority=6,
        next_collect_at=now
    ),
    NewsKeyword(
        keyword="금리 인하",
        priority=7,
        next_collect_at=now
    ),
]

class NewsKeywordRepository:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def find_collect_targets(
            self,
            now: datetime,
            limit: int = 10
    ) -> list[NewsKeyword]:
        with self.session_factory() as db:
            stmt = (
                select(NewsKeyword)
                .where(
                    NewsKeyword.next_collect_at <= now,
                )
                .order_by(
                    NewsKeyword.priority.desc()
                )
                .limit(limit)
            )
            result = db.scalars(stmt)
            return list(result)
        
    def update_next_collect_at(
            self,
            keyword_id: int,
            next_collect_at: datetime
    ) -> None:
        with self.session_factory() as db:
            stmt = (
                update(NewsKeyword)
                .where(
                    NewsKeyword.id == keyword_id
                )
                .values(
                    next_collect_at=next_collect_at
                )
            )
            db.execute(stmt)
            db.commit()

    def save(self, keyword: NewsKeyword) -> NewsKeyword:
        with self.session_factory() as db:
            db.add(keyword)
            db.commit()
            db.refresh(keyword)

            return keyword

    def initialize(self):
        with self.session_factory() as db:
            db.add_all(keywords)
            db.commit()