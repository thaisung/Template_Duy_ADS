from ...models import *

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator


from django.http import HttpResponse
import requests
import time

from django.db import models
from django.utils import timezone

import os

from datetime import datetime

from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import datetime
from django.contrib import messages
import random
import string
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

# from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

import random
import string

import base64

import time
from django.http import JsonResponse

import re
import json

from django.conf import settings
from django.db.models import Q

import datetime

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


import base64

from django.utils.timezone import localtime


    
def content_admin(request):
    if request.method == 'GET':
        context = {}
        context['domain'] = settings.DOMAIN
        
        # Lấy danh sách content, sắp xếp mới nhất trước
        list_content = Content.objects.all().order_by('-id')
        
        s = request.GET.get('s')
        if s:
            list_content = list_content.filter(Q(content__icontains=s))
            context['s'] = s
        
        # Phân trang 15 bản ghi/trang
        paginator = Paginator(list_content, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        context['list_Content'] = page_obj
        context['page_obj'] = page_obj
        context['content_pages'] = ['content_admin', 'content_add_admin', 'content_edit_admin']
        
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, 'sleekweb/admin/content_admin.html', context, status=200)
        else:
            return redirect('login_admin')
        

def content_add_admin(request):
    if request.method == 'GET':
        context = {}
        context['domain'] = settings.DOMAIN
        # print('context:',context)
        context['content_pages'] = [ 'content_admin', 'content_add_admin', 'content_edit_admin']
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, 'sleekweb/admin/content_add_admin.html', context, status=200)
        else:
            return redirect('login_admin')
        
    elif request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            fields = {}
            content = request.POST.get('content', '')
            content = content.strip()
            fields['content'] = content
            obj = Content.objects.create(**fields)
            return redirect('content_admin')
        else:
            return redirect('login_admin')
    
def content_edit_admin(request,pk):
    if request.method == 'GET':
        context = {}
        context['domain'] = settings.DOMAIN
        context['obj_Content'] = Content.objects.get(pk=pk)
        # print('context:',context)
        context['content_pages'] = [ 'content_admin', 'content_add_admin', 'content_edit_admin']
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, 'sleekweb/admin/content_edit_admin.html', context, status=200)
        else:
            return redirect('login_admin')
    elif request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            fields = {}
            fields['content'] = request.POST.get('content')

            obj = Content.objects.get(pk=pk)
            obj.Title = fields['content']

            obj.save()
            return redirect('content_edit_admin',pk=pk)
        else:
            return redirect('login_admin')
    
def content_remove_admin(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            try:
                obj = Content.objects.get(pk=pk)
                obj.delete()
            except:
                print('not')
            return redirect('content_admin')
    else:
        return redirect('login_admin')
        
def copy_log(request):
    if request.method == 'POST':
        content_id = request.POST.get("content_id")
        log = CopyLog.objects.create(content_id=content_id)
        # Trả về content_id và copied_at để frontend cập nhật giao diện
        return JsonResponse({
            "status": "ok",
            "content_id": content_id,
            "copied_at": localtime(log.copied_at).strftime("%d/%m/%Y %H:%M:%S")
        })

def get_copy_logs(request):
    """API để frontend polling lấy danh sách copy logs"""
    if request.method == 'GET':
        contents = Content.objects.all()
        data = {}
        for content in contents:
            logs = content.copy_logs.all().order_by('-copied_at')[:20]  # Lấy 20 bản ghi mới nhất
            data[content.id] = [localtime(log.copied_at).strftime("%d/%m/%Y %H:%M:%S") for log in logs]
        return JsonResponse({"copy_logs": data})
