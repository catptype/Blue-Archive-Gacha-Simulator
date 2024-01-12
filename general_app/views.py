from django.shortcuts import render

def home(request):
    return render(request, 'general_app/index.html')

def about(request):
    return render(request, 'general_app/about.html')