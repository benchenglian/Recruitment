###
 # @Author: Frank.Lian
 # @Description: 
 # @Date: 2021-09-09 18:03:00
 # @LastEditTime: 2021-09-09 18:05:25
 # @FilePath: /recruitment/worker.start.sh
 # @Author: ic1129-x0
### 
# 启动 recruitment 这个 package 的时候，会运行 __init__.py
# __init__.py 里面初始化了 django 的配置
DJANGO_SETTINGS_MODULE=settings.local celery -A recruitment worker -l INFO