'''
Author: Frank.Lian
Description: 
Date: 2021-05-04 22:29:01
LastEditTime: 2021-09-10 16:51:33
FilePath: /recruitment/recruitment/urls.py
'''
"""recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from job.models import Job
from django.utils.translation import gettext as _
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path("",include("job.urls")),
    # django rest api & api auth (login/logout)
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    #path('admin/#/admin/interview/candidate/', trigger_error),
    #path('simpleui/',include('simpleui.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('registration.backends.simple.urls')),
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


admin.site.site_header = _('Inmobi??????????????????')