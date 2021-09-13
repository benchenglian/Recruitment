'''
Author: Frank.Lian
Description: 
Date: 2021-09-07 17:30:05
LastEditTime: 2021-09-09 18:15:54
FilePath: /recruitment/celery/tasks.py
Author: ic1129-x0
'''
#!coding=utf-8

from celery import Celery

# 第一个参数 是当前脚本的名称，第二个参数 是 broker 服务地址
app = Celery('tasks', backend='redis://127.0.0.1', broker='redis://127.0.0.1')

@app.task
def add(x, y):
    return x + y
