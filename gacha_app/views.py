from django.shortcuts import render, get_object_or_404
from .models import GachaBanner

def gacha(request):
    banners = GachaBanner.objects.all()
    context = {
        'banners': banners,
        'rarities': [3,2,1],
    }    
    return render(request, 'gacha_app/gacha.html', context)

def gacha_detail(request, gacha_id):
    banner = get_object_or_404(GachaBanner, pk=gacha_id)
    context = {
        'banner': banner,
        'gacha_id': gacha_id,
        'rarities': [3,2,1],
    }
    return render(request, 'gacha_app/gacha_detail.html', context)

