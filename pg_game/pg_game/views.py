from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def login_form(request):
    """ Вывод страницы авторизации"""
    if not request.user.is_authenticated:
        return render(request, 'auth/login.html')
    else:
        return redirect('/')


def login_save(request):
    """ Авторизация пользователя"""
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = str.lower(request.POST.get('username', ''))
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password, request=request)
        if user and user.is_active:
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Неправильные логин или пароль')
            return redirect('login_form')
    else:
        logout(request)
        return redirect('login_form')
