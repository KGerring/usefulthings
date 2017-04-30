#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = scheduler
# author=AutisticScreeching
# date = 3/15/17
import sys, os
from pytz import utc


import apscheduler
import apscheduler.events
import apscheduler.executors
import apscheduler.executors.asyncio
import apscheduler.executors.base
import apscheduler.executors.base_py3
import apscheduler.executors.debug
import apscheduler.executors.gevent
import apscheduler.executors.pool
import apscheduler.executors.tornado
import apscheduler.executors.twisted
import apscheduler.job
import apscheduler.jobstores
import apscheduler.jobstores.base
import apscheduler.jobstores.memory
import apscheduler.jobstores.mongodb
import apscheduler.jobstores.redis
import apscheduler.jobstores.sqlalchemy
import apscheduler.schedulers
import apscheduler.schedulers.asyncio
import apscheduler.schedulers.background
import apscheduler.schedulers.base
import apscheduler.schedulers.blocking
import apscheduler.schedulers.gevent
import apscheduler.schedulers.qt
import apscheduler.schedulers.tornado
import apscheduler.schedulers.twisted
import apscheduler.triggers
import apscheduler.triggers.base
import apscheduler.triggers.cron
import apscheduler.triggers.cron.expressions
import apscheduler.triggers.cron.fields
import apscheduler.triggers.date
import apscheduler.triggers.interval
import apscheduler.util

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.redis import RedisJobStore, StrictRedis
EVERY_30_SECONDS = apscheduler.triggers.interval.IntervalTrigger(seconds=30,
                                                                 end_date='2017-03-23 22:26:25 EDT')


jobstores = {
	'memory': MemoryJobStore(),
	'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

executors = {
	'default':     ThreadPoolExecutor(20),
	'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
	'coalesce':      False,
	'max_instances': 3
}

#Of the builtin job stores, only MemoryJobStore doesn’t serialize jobs.
# Of the builtin executors, only ProcessPoolExecutor will serialize jobs.
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors,
                                job_defaults=job_defaults, timezone=utc)


def my_listener(event):
	if event.exception:
		print('The job crashed :(')
	else:
		print('The job worked :)')


scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)




#If you schedule jobs in a persistent job store during your application’s initialization,
# you MUST define an explicit ID for the job and use replace_existing=True or you will get a
# new copy of the job every time your application restarts!

#/Users/kristen/.bash_sessions/0E457946-31DC-4397-8B11-309D300A1524.history

#func_name
#to_dict

	
if __name__ == '__main__':
	scheduler = BackgroundScheduler()
