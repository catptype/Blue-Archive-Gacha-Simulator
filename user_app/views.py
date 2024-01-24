from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .utils import user_authenticated, DashboardContent
from .forms import CreateNewUserForm, LoginForm, ForgotPasswordForm

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
    return redirect('/')

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
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['password1']

            # Retrieve the user and update the password
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            messages.success(request, 'Password updated successfully.')
            return redirect('login')  # Redirect to your login page

    else:
        form = ForgotPasswordForm()
    
    context = {
        'form': form,
    }
    return render(request, 'user_app/forgot.html', context)


    if request.user.is_authenticated:
        return redirect('/user/dashboard')

    return render(request, 'user_app/forget.html')

@user_authenticated
def dashboard(request):
    tab = request.GET.get('tab', None)
    
    if tab == 'history':
        context = {
            'html_content': DashboardContent.history(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'statistic':
        context = {
            'html_content': DashboardContent.statistic(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'collection':
        context = {
            'html_content': DashboardContent.collection(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'achievement':
        context = {
            'html_content': DashboardContent.achievement(request),
        }
        return render(request, 'user_app/dashboard.html', context)
    
    elif tab == 'change-password':
        context = {
            'html_content': DashboardContent.change_password(request),
        }
        return render(request, 'user_app/dashboard.html', context)

    return render(request, 'user_app/dashboard.html')