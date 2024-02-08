from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest

from .models import GachaBanner
from .utils import GachaSystem

def gacha(request):
    banners = GachaBanner.objects.all()
    context = {
        'banners': banners,
        'banner_idx': range(banners.count()),
    }    
    return render(request, 'gacha_app/gacha.html', context)

def gacha_detail(request, gacha_id):
    banner = get_object_or_404(GachaBanner, pk=gacha_id)
    user_instance = request.user
    gacha_instance = GachaSystem(user_instance, banner)
    num_guarantee = gacha_instance.get_guarantee_rarity3()
    context = {
        'banner': banner,
        'gacha_id': gacha_id,
        'rarities': [3, 2, 1],
        'num_draws': [1, 10],
        'num_guarantee': num_guarantee + 1,
        'is_auth': user_instance.is_authenticated,
    }
    return render(request, 'gacha_app/detail.html', context)

def gacha_result(request, gacha_id):
    banner = get_object_or_404(GachaBanner, pk=gacha_id)

    if request.method == 'POST':
        
        user_instance = request.user
        num_draw = int(request.POST.get('draw'))

        if num_draw not in [1, 10]:
            return HttpResponseBadRequest("Invalid draw option")
        
        gacha_instance = GachaSystem(user_instance, banner)
        drawn_students = gacha_instance.draw_gacha(num_draw)
        new_students = gacha_instance.get_new_students(drawn_students)
        num_guarantee = gacha_instance.get_guarantee_rarity3()
        gacha_instance.save_transaction(drawn_students)

        context = {
            'banner': banner,
            'gacha_id': gacha_id,
            'rarities': [3, 2, 1],
            'drawn_students': drawn_students,
            'num_draw': num_draw,
            'new_students': new_students,
            'num_guarantee': num_guarantee + 1,
            'is_auth': user_instance.is_authenticated,
        }
        return render(request, 'gacha_app/result.html', context)
    
    else:
        return HttpResponseBadRequest("SOMETHING WRONG")