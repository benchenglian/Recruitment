'''
Autor: Frank.Lian
Description: 
Date: 2021-05-04 22:29:01
LastEditTime: 2021-09-09 09:58:23
FilePath: /recruitment/recruitment/__init__.py
Author: ic1129-x0
'''
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)