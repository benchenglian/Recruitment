'''
Autor: Frank.Lian
Description: 
Date: 2021-09-07 17:36:24
LastEditTime: 2021-09-07 17:36:58
FilePath: /recruitment/celery/run_task.py
Author: ic1129-x0
'''
from tasks import add 
result = add.delay(4, 4)
print('Is task ready: %s' % result.ready())

run_result = result.get(timeout=1)
print('task result: %s' % run_result)