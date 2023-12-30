from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import CreateNewUserForm, LoginForm
from gacha_app.models import GachaTransaction

from .utils.user_authenticated import user_authenticated

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
def history(request):
    transactions = GachaTransaction.objects.filter(user=request.user).order_by('-id')

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page', 1)

    # Use Django's Paginator to paginate the transactions
    paginator = Paginator(transactions, 10)

    try:
        # Get the transactions for the requested page
        transactions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        transactions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        transactions = paginator.page(paginator.num_pages)

    context = {
        'transactions': transactions,
    }
        
    return render(request, 'user_app/history.html', context)

@user_authenticated
def statistic(request):
    return render(request, 'user_app/statistic.html')

@user_authenticated
def change_password(request):
    return render(request, 'user_app/change_password.html')