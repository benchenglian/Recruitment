#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2021/08/26  6:32 下午
@Author  : Frank.lian
@File    : dingtalk.py
@Description :
'''
from dingtalkchatbot.chatbot import DingtalkChatbot
from django.conf import settings
def send(messge,at_mobiles=[]):
    # 引用settings里面配置的钉钉群消息同志的WebHook地址：
    webhook = settings.DINGTALK_WEB_HOOK

    # 初始化机器人小钉 ，#方法一：通常初始化方法
    xiaoding = DingtalkChatbot(webhook)

    # 方式二：勾选"加签"选项使用（v1.5以上新功能）
    # xiaoding = DingtalkChatbot(webhook,secret=secret)

    # Text消息所有人
    xiaoding.send_text(msg=('面试通知：%s' % messge),at_mobiles = at_mobiles)