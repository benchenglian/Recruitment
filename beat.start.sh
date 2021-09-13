###
 # @Author: Frank.Lian
 # @Description: 
 # @Date: 2021-09-09 18:14:43
 # @LastEditTime: 2021-09-09 18:24:59
 # @FilePath: /recruitment/beat.start.sh
 # @Author: ic1129-x0
### 
# DJANGO_SETTINGS_MODULE=settings.local celery -A recruitment beat 
DJANGO_SETTINGS_MODULE=settings.local celery -A recruitment beat --scheduler django_celery_beat.schedulers:DatabaseScheduler