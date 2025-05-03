from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.models import Hotel
from django.http import HttpResponseRedirect, JsonResponse

import logging
logger = logging.getLogger('__name__')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username = username , password = password)
        if not user_obj:
            messages.warning(request, 'Invalid password ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request , user_obj)
        return redirect('/')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request ,'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter( Q(username=username) | Q(email=email)).exists():
            messages.warning(request, 'Username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(username = username, email = email)
        user.set_password(password)
        user.save()
        return redirect('/')

    return render(request , 'register.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")

