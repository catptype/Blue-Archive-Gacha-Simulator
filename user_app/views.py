from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from functools import wraps
from .forms import CreateNewUserForm, LoginForm

def user_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('HTTP403: You do not have permission to access this page.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateNewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('register_complete')
        else:
            print(form.error_messages)
    else:
        form = CreateNewUserForm()

    context = {
        'form': form,
    }
    return render(request, 'user_app/register.html', context)

def register_complete(request):
    return render(request, 'user_app/register_complete.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/user/dashboard')
    else:
        form = LoginForm()
    
    context = {
        'form': form,
    }
    return render(request, 'user_app/login.html', context)

def forget(request):
    if request.user.is_authenticated:
        return redirect('/user/dashboard')

    return render(request, 'user_app/forget.html')

@user_authenticated
def dashboard(request):    
    return render(request, 'user_app/dashboard.html')

@user_authenticated
def setting(request):
    return render(request, 'user_app/setting.html')