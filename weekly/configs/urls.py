#coding:utf-8

from django.conf.urls import include, url


urlpatterns = [
   url(r'^report/', include('report.urls'))
]