#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
from django.http import HttpResponse
import traceback

from sentry_sdk import capture_exception
from . import dingtalk

'''
@Time    : 2021/09/01  1:56 下午
@Author  : Frank.lian
@File    : performance.py
@Description :
'''
logger = logging.getLogger(__name__)
def performance_logger_middleware(get_response):
    def middleware(request):
        start_time = time.time()
        response = get_response(request)
        duration = time.time() - start_time
        response["X-page-Duration-ms"] = int(duration * 1000) # 通过相应头返回。
        logger.info("%s %s %s",duration,request.path,request.GET.dict()) # 耗时、路径、参数
        return response
    return middleware


class PerformanceAndExceptionLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        response["X-Page-Duration-ms"] = int(duration * 1000)
        logger.info("duration:%s url:%s parameters:%s", duration, request.path, request.GET.dict())
        if duration > 300: # 页面超过300毫秒上报
            capture_exception("slow request for url:%s with duration:%s" %(request.build_absolute_uri(),duration))

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        if exception:
            message = "url:{url} ** msg:{error} ````{tb}````".format(
                url=request.build_absolute_uri(),
                error=repr(exception),
                tb=traceback.format_exc()
            )

            logger.warning(message)

            # send dingtalk message
            dingtalk.send(message)

            # capture exception to sentry:
            capture_exception(exception)

        return HttpResponse("Error processing the request, please contact the system administrator.", status=500)