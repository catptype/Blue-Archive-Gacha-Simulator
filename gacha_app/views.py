# views.py
from django.shortcuts import render

# Create your views here.
def gacha(request):
    return render(request, 'gacha_app/gacha.html')
