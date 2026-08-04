from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.container import container

app = FastAPI()

scheduler = BackgroundScheduler()


def collect_news_job(priority: list[int]):
    news_service = container.news_collect_service
    for p in priority:
        news_service.collect_news_with_priority(p)


def register_jobs():

    scheduler.add_job(
        collect_news_job,
        'cron',
        minute='10',
        args=[[9, 10]],
        id='news_collect_9_10',
        replace_existing=True
    )

    scheduler.add_job(
        collect_news_job,
        'cron',
        minute='30',
        args=[[7, 8]],
        id='news_collect_7_8',
        replace_existing=True
    )

    scheduler.add_job(
        collect_news_job,
        'cron',
        hour='2',
        args=[[5, 6]],
        id='news_collect_5_6',
        replace_existing=True
    )

    scheduler.add_job(
        collect_news_job,
        'cron',
        hour='12',
        args=[[3, 4]],
        id='news_collect_3_4',
        replace_existing=True
    )

    scheduler.add_job(
        collect_news_job,
        'cron',
        hour='48',
        args=[[1, 2]],
        id='news_collect_1_2',
        replace_existing=True
    )


def start_scheduler():
    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown()