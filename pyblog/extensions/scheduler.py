import datetime
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler


def add_one_time_job(func: Callable, args: tuple, delete_after: datetime.timedelta):
    sched = BackgroundScheduler(daemon=True)
    run_date = datetime.datetime.now() + delete_after
    sched.add_job(func, 'date', run_date=run_date, args=args)
    sched.start()
