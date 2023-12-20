from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

from .forms import CreateNewUserForm, LoginForm

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

    context = {'form':form}
    return render(request, 'user_app/register.html', context)

def register_complete(request):
    return render(request, 'user_app/register_complete.html')

def user_logout(request):
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
                return redirect('/')
    else:
        form = LoginForm()
    
    context = {'form':form}
    return render(request, 'user_app/login.html', context)

def forget(request):
    return render(request, 'user_app/forget.html')