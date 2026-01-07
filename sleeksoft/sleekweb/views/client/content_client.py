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



    
def content_client(request):
    if request.method == 'GET':
        context = {}
        context['domain'] = settings.DOMAIN
        
        # Lấy danh sách content, sắp xếp mới nhất trước
        list_content = Content.objects.all().order_by('-id')
        
        s = request.GET.get('s')
        if s:
            list_content = list_content.filter(Q(title__icontains=s))
            context['s'] = s
        
        # Phân trang 15 bản ghi/trang
        paginator = Paginator(list_content, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        context['list_Content'] = page_obj
        context['page_obj'] = page_obj
        
        return render(request, 'sleekweb/client/content_client.html', context, status=200)


def content_detail_client(request, slug):
    """Hiển thị trang content riêng cho mỗi client"""
    if request.method == 'GET':
        context = {}
        context['domain'] = settings.DOMAIN
        
        # Lấy content theo slug
        content_obj = get_object_or_404(Content, slug=slug)
        context['content'] = content_obj
        
        # Lấy tất cả lines và phân trang 50 dòng/trang
        all_lines = content_obj.lines.all().order_by('order')
        paginator = Paginator(all_lines, 50)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        context['lines'] = page_obj
        context['page_obj'] = page_obj
        
        return render(request, 'sleekweb/client/content_detail_client.html', context, status=200)
