#coding:utf-8

import json

from django.http import HttpResponse
from django.shortcuts import redirect


class JSONResponse(HttpResponse):
    """JSON response class."""

    def __init__(self, obj='', json_opts={}, mimetype="application/json", *args, **kwargs):
        content = json.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


def login_required_by_render(func):
	def wrapped_fuc(request, *args, **kwargs):
		user = request.request.user

		if not user.is_authenticated():
			return redirect('/report/login')
		else:
			return func(request, *args, **kwargs)
	return wrapped_fuc


def login_required_by_ajax(func):
	def wrapped_fuc(request, *args, **kwargs):
		user = request.request.user

		if not user.is_authenticated():
			return JSONResponse({'code': -2, 'error': '当前位登录'})
		else:
			return func(request, *args, **kwargs)
	return wrapped_fuc


def is_superuser(func):
	def wrapped_fuc(request, *args, **kwargs):
		user = request.request.user

		if not user.is_authenticated() or not user.is_superuser:
			return JSONResponse({'code': -2, 'error': '不是超级管理员'})
		else:
			return func(request, *args, **kwargs)
	return wrapped_fuc