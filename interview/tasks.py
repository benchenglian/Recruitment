'''
Author: Frank.Lian
Description: 
Date: 2021-09-09 10:09:47
LastEditTime: 2021-09-09 10:11:13
FilePath: /recruitment/interview/tasks.py
Author: ic1129-x0
'''
from __future__ import absolute_import, unicode_literals

from celery import shared_task 
from .dingtalk import send

@shared_task
def send_dingtalk_message(message):
    send(message)