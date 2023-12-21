from django.shortcuts import render

def gacha(request):
    return render(request, 'gacha_app/gacha.html')
