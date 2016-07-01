#coding:utf-8

from enum import Enum
from collections import OrderedDict

from django.db import models
from django.contrib.auth.models import User


class Department(Enum):
	other = 0
	develop = 1
	ui = 2
	pm = 3
	operate = 4


department_dict = OrderedDict([
	(Department.develop, '技术'),
	(Department.ui, '设计'),
	(Department.pm, '产品'),
	(Department.operate, '运营'),
	(Department.other, '其他')
])


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	department = models.SmallIntegerField(default=Department.other)


class Report(models.Model):
	user = models.ForeignKey(User, related_name="report")
	weekly_num = models.IntegerField()
	create_time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%sat%s' % (self.user.username, self.create_time)


class ReportContent(models.Model):
	user = models.ForeignKey(User, related_name="ReportContent")
	report = models.ForeignKey(Report, related_name="ReportContent")
	contents = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s had write report' % self.user.username
