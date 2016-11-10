#coding:utf-8

import datetime
import time

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.http import Http404

from utils import JSONResponse, login_required_by_render, login_required_by_ajax, is_superuser
from models import department_dict, UserProfile, Report, ReportContent


class Login(View):
	TEMPLATE = 'login.html'

	def get(self, request):
		if request.user.is_authenticated():
			return redirect('/report/')

		return render(request, self.TEMPLATE, locals())

	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if not user:
			raise Http404
		else:
			login(request, user)
			return redirect('/report/')


class Logout(View):
	def get(self, request):
		logout(request)
		return redirect('/report/login')


class Regist(View):
	TEMPLATE = 'register.html'

	def get(self, request):
		data = {}
		data['department'] = department_dict

		return render(request, self.TEMPLATE, data)

	def post(self, request):
		username = request.POST.get('username')
		password = make_password(request.POST.get('password'))
		department = request.POST.get('department', 0)

		user = User.objects.create(username=username, password=password)
		UserProfile.objects.create(user=user, department=int(department))
		return redirect('/report/login')


class MakeReportMain(View):
	TEMPLATE = 'report_main.html'

	@login_required_by_render
	def get(self, request):
		_data = {}

		_data['report'] = Report.objects.all().order_by('-create_time')
		return render(request, self.TEMPLATE, _data)

	@is_superuser
	def post(self, request):

		today = datetime.date.today()

		is_ex = Report.objects.filter(create_time__startswith=today).exists()
		if not is_ex:
			Report.objects.create(user=request.user, weekly_num=time.strftime('%W'))
		else:
			return JSONResponse({'code': -1, 'error': u'已经创建过了'})

		return JSONResponse({'code': 0})


class ReportContents(View):
	TEMPLATE = 'report_contents.html'

	@login_required_by_render
	def get(self, request, report_id):
		_data = {}
		report = Report.objects.get(id=report_id)

		_data['report_contents'] = ReportContent.objects.filter(report=report)
		return render(request, self.TEMPLATE, _data)

	@login_required_by_ajax
	def post(self, request, report_id):
		report = Report.objects.get(id=report_id)
		mode = request.POST.get('mode')
		if mode == 'check':
			if ReportContent.objects.filter(user=request.user, report=report).exists():
				return JSONResponse({'code': -1, 'error': u'已经写过周报了'})
			else:
				return JSONResponse({'code': 0})
		elif mode == 'save':
			contents = request.POST.get('contents')
			ReportContent.objects.create(user=request.user, report=report, contents=contents)
			return JSONResponse({'code': 0})
		else:
			return JSONResponse({'code': -4, 'error': u'未知错误'})
