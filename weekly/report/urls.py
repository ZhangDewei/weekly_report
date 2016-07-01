#coding:utf-8

from django.conf.urls import url

from views import Login, Regist, MakeReportMain, Logout, ReportContents

urlpatterns = [
	url(r'^login/$', Login.as_view(), name='login'),
	url(r'^logout/$', Logout.as_view(), name='logout'),
	url(r'^regist/$', Regist.as_view(), name='regist'),
	url(r'^$', MakeReportMain.as_view(), name='report_main'),
	url(r'^report_contents/(?P<report_id>\d+)/', ReportContents.as_view())
]