'''
Autor: [you name]
Description: 
Date: 2021-05-04 22:29:01
LastEditTime: 2021-09-06 14:24:53
'''
"""
ASGI config for recruitment project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recruitment.settings')

application = get_asgi_application()
