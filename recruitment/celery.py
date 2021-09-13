'''
Author: Frank.Lian
Description: 
Date: 2021-09-07 23:02:54
LastEditTime: 2021-09-10 15:18:51
FilePath: /recruitment/recruitment/celery.py
Author: ic1129-x0
'''
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery, shared_task

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

app = Celery('recruitment')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# from celery.schedules import crontab, schedule

# #this is important to load the celery tasks
# from recruitment.tasks import add
# # 注意下面引用的tasks.add 的方法，必须显示import，才能正确注册。
# app.conf.beat_schedule = {# 在代码中配置有哪些任务要跑。
#     'add-every-10-seconds': {
#         'task': 'recruitment.tasks.add',
#         'schedule': 10.0,
#         'args': (16, 4, )
#     },
# }

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='hello every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

# import json
# from django_celery_beat.models import PeriodicTask,IntervalSchedule
# # 先创建定时策略
# schedule, created = IntervalSchedule.objects.get_or_create(every=10,period=IntervalSchedule.SECONDS,)

# # 再创建任务 interval上面设置的schedule，name是任务名称，task调用celery的test方法，参数传递json格式的文本。
# task = PeriodicTask.objects.create(interval=schedule,name='say welcome 2021' ,task = 'recruitment.celery.test',args=json.dumps(['welcome'] ), )
 
@app.task
def test(arg):
    print(arg)


app.conf.timezone = "Asia/Shanghai"