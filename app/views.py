from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

# Create your views here.


def home(request):
    return render(request, 'home.html')


def create(request):
    return render(request, 'create.html')


def store(request):
    data = {}
    if request.POST['password'] != request.POST['password-conf']:
        data['msg'] = 'Senhas digitadas diferentes'
        data['class'] = 'alert-danger'
    else:
        data['msg'] = 'Usuário cadastrado com sucesso'
        data['class'] = 'alert-success'
        user = User.objects.create_user(request.POST['user'], request.POST['email'], request.POST['password'])
        user.save()
    return render(request, 'create.html', data)


def painel(request):
    return render(request, 'painel.html')


def dologin(request):
    data = {}
    user = authenticate(username=request.POST['user'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect('/dashboard')
    else:
        data['msg'] = 'Nome de usuário e/ou senha incorretos.'
        data['class'] = 'alert-danger'
        return render(request, 'painel.html', data)


def dashboard(request):
    return render(request, 'dashboard/home.html')


def logouts(request):
    logout(request)
    return redirect('/painel')

def setpass(request):
    return render(request, 'setpass.html')


def changePassword(request):
    data = {}
    if request.POST['password'] == request.POST['password-conf']:
        u = User.objects.get(email=request.user.email)
        u.set_password(request.POST['password'])
        u.save()
        logout(request)
        return redirect('/painel/')
    else:
        data['msg'] = 'Você digitou duas senhas erradas'
        data['class'] = 'alert-danger'
        return render(request, 'setpass.html', data)