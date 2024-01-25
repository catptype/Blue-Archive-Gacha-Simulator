from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed

from .utils import user_authenticated, DashboardContent
from .forms import CreateNewUserForm, LoginForm, ForgotPasswordForm

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = CreateNewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('register_complete')
    else:
        form = CreateNewUserForm()

    context = {'form': form}
    return render(request, 'user_app/register.html', context)

def register_complete(request):
    return redirect('/')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'user_app/login.html', context)

def forget(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['password1']
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('login')
    else:
        form = ForgotPasswordForm()
    
    context = {'form': form}
    return render(request, 'user_app/forgot.html', context)

@user_authenticated
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    else:
        return HttpResponseNotAllowed(['POST'])
    
@user_authenticated
def dashboard(request):
    tab = request.GET.get('tab', None)
    
    if tab == 'history':
        context = {'html_content': DashboardContent.history(request)}
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'statistic':
        context = {'html_content': DashboardContent.statistic(request)}
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'collection':
        context = {'html_content': DashboardContent.collection(request)}
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'achievement':
        context = {'html_content': DashboardContent.achievement(request)}
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'change-password':
        context = {'html_content': DashboardContent.change_password(request)}
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'reset':
        context = {'html_content': DashboardContent.reset_account(request)}
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'delete':
        context = {'html_content': DashboardContent.delete_account(request)}
        return render(request, 'user_app/dashboard.html', context)
    else:
        return render(request, 'user_app/dashboard.html')