'''
Author: Frank.Lian
Description: 
Date: 2021-09-09 19:02:12
LastEditTime: 2021-09-09 19:02:12
FilePath: /recruitment/recruitment/tasks.py
'''
from __future__ import absolute_import, unicode_literals
from celery import shared_task 

@shared_task
def add(a, b,):
    return a + b