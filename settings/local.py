'''
Autor: Frank.Lian
Description: 
Date: 2021-05-10 19:20:17
LastEditTime: 2021-09-09 10:08:49
FilePath: /recruitment/settings/local.py
'''
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

ALLOWED_HOSTS = ['127.0.0.1']

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "TIMEOUT": 300,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            #"PASSWORD": "mysecret",
            "SOCKET_CONNECT_TIMEOUT": 5, # in seconds
            "SOCKET_TIMEOUT":5, # r/w timeout in seconds 
        }
    }
}

# Celery application definition
CELERY_BROKER_URL = "redis://localhost:6379/0" #消息代理
CELERY_RESULT_BAKEND = "redis://localhost:6379/1" # 运行结果
CELERY_ACCETP_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_MAX_TASKS_PER_CHILD = 10
CELERY_LOG_FILE = os.path.join(BASE_DIR,"logs","celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR,"logs","celery_beat.log")

LDAP_AUTH_CONNECTION_USERNAME = "CN=admin,DC=ihopeit,DC=com"
LDAP_AUTH_CONNECTION_PASSWORD = "admin_passwd_4_ldap"

LDAP_AUTH_URL = "ldap://0.0.0.0:389"

SECRET_KEY = '5s=i#n34&%l0n)e3dajb(@!(8--ksrkxlhb8%#_@p_-oj*@_rh'

DINGTALK_WEB_HOOK = "https://oapi.dingtalk.com/robot/send?access_token=608ed3b09121834dedbcbd2931379e96fc2fbd743c8bf083e7237c6818a5fb1b"

DEBUG = True

INSTALLED_APPS += ()

sentry_sdk.init(
    dsn="http://631d5f835f6f4767889f0655d875f3a3@101.200.131.229:9000/3",
    integrations=[DjangoIntegration()],
    # performance tracing sample rate,采样率，生产环境访问量过大时，建议调小（不用每一个URL请求都记录性能）
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True # 是否发送个人标识信息。
)
