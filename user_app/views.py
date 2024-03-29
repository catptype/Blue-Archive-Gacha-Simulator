from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.utils.html import format_html

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
            return render(request, 'user_app/register_complete.html')
    else:
        form = CreateNewUserForm()

    context = {'form': form}
    return render(request, 'user_app/register.html', context)

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
        context = {
            'dashboard_title': format_html('<h1>HISTORY</h1>'),
            'html_content': DashboardContent.history(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'statistic':
        context = {
            'dashboard_title': format_html('<h1>STATISTIC</h1>'),
            'html_content': DashboardContent.statistic(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'collection':
        context = {
            'dashboard_title': format_html('<h1>COLLECTION</h1>'),
            'html_content': DashboardContent.collection(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'achievement':
        context = {
            'dashboard_title': format_html('<h1>ACHIEVEMENT</h1>'),
            'html_content': DashboardContent.achievement(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'change-password':
        context = {
            'dashboard_title': format_html('<h1>CHANGE PASSWORD</h1>'),
            'html_content': DashboardContent.change_password(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'reset':
        context = {
            'dashboard_title': format_html('<h1>RESET ACCOUNT</h1>'),
            'html_content': DashboardContent.reset_account(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'delete':
        delete_flag, html_content = DashboardContent.delete_account(request)
        if delete_flag:
            return redirect('/')
        else:
            context = {
                'dashboard_title': format_html('<h1>DELETE ACCOUNT</h1>'),
                'html_content': html_content,
            }
            return render(request, 'user_app/dashboard.html', context)
    
    elif tab is None:
        html_content = DashboardContent.welcome(request)

        context = {
            'dashboard_title': format_html('<h1>WELCOME</h1>'),
            'html_content': html_content,
        }
        return render(request, 'user_app/dashboard.html', context)
    
    else:
        html_content = DashboardContent.not_found(request)
        context = {
            'dashboard_title': format_html('<h1>NOT FOUND</h1>'),
            'html_content': html_content,
        }
        return render(request, 'user_app/dashboard.html', context)