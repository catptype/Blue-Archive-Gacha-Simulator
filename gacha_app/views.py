from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest

from .models import GachaBanner
from .utils import GachaSystem

from django.core.serializers import serialize, deserialize


def gacha(request):
    banners = GachaBanner.objects.all()
    context = {
        'banners': banners,
        'banner_idx': range(banners.count()),
    }    
    return render(request, 'gacha_app/gacha.html', context)

def gacha_detail(request, gacha_id):
    banner = get_object_or_404(GachaBanner, pk=gacha_id)
    context = {
        'banner': banner,
        'gacha_id': gacha_id,
        'rarities': [3, 2, 1],
        'num_draws': [1, 10],
    }
    return render(request, 'gacha_app/gacha_detail.html', context)

def gacha_result(request, gacha_id):
    banner = get_object_or_404(GachaBanner, pk=gacha_id)

    if request.method == 'POST':
        num_draw = int(request.POST.get('draw'))

        if num_draw not in [1, 10]:
            return HttpResponseBadRequest("Invalid draw option")
        
        gacha_instance = GachaSystem(request.user, banner)
        drawn_students = gacha_instance.draw_gacha(num_draw)
        gacha_instance.save_transaction(drawn_students)

        context = {
            'banner': banner,
            'gacha_id': gacha_id,
            'rarities': [3, 2, 1],
            'drawn_students': drawn_students,
            'num_draw': num_draw,
        }
        return render(request, 'gacha_app/gacha_result.html', context)
    else:
        return redirect('gacha_detail', gacha_id=gacha_id)
