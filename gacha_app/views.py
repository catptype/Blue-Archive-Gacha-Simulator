import random
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import GachaBanner

def gacha(request):
    banners = GachaBanner.objects.all()
    context = {
        'banners': banners,
    }    
    return render(request, 'gacha_app/gacha.html', context)

def gacha_detail(request, gacha_id):
    banner = get_object_or_404(GachaBanner, pk=gacha_id)
    context = {
        'banner': banner,
        'gacha_id': gacha_id,
        'rarities': [3, 2, 1],
    }
    return render(request, 'gacha_app/gacha_detail.html', context)

def gacha_result(request, gacha_id):
    banner = get_object_or_404(GachaBanner, pk=gacha_id)

    if request.method == 'POST':
        if 'draw_1' in request.POST:
            num_draw = 1
            result = draw_gacha(banner, 1)
        elif 'draw_10' in request.POST:
            num_draw = 10
            result = draw_gacha(banner, 10)
        elif 'draw_100' in request.POST:
            num_draw = 100
            result = draw_gacha(banner, 100)
        else:
            result = []

        context = {
            'banner': banner,
            'gacha_id': gacha_id,
            'rarities': [3, 2, 1],
            'result': result,
            'num_draw': num_draw,
        }
        return render(request, 'gacha_app/gacha_result.html', context)
    else:
        return redirect('gacha_detail', gacha_id=gacha_id)
    

def draw_gacha(banner, num_draws):
    pickup_rate = 1.0
    rates = {
        3: float(banner.rate_3_star), 
        2: float(banner.rate_2_star), 
        1: float(banner.rate_1_star),
    }

    student_pickup = list(banner.is_pickup.all())
    students_by_rarity = {
        3: list(banner.not_pickup.filter(rarity=3)),
        2: list(banner.not_pickup.filter(rarity=2)),
        1: list(banner.not_pickup.filter(rarity=1)),
    }

    counter = {}
    drawn_characters = []

    result_list = random.choices(list(rates.keys()), list(rates.values()), k=num_draws)
    for result in result_list:
        
        counter[result] = counter.get(result, 0) + 1

        if result == 3 and banner.is_pickup.all():
            all_students = student_pickup + students_by_rarity[result]
            pickup_weights = [pickup_rate / len(student_pickup)] * len(student_pickup)
            not_pickup_weight = [(rates[result] - pickup_rate) / len(students_by_rarity[result])] * len(students_by_rarity[result])
            all_weights = pickup_weights + not_pickup_weight
        
        else:
            all_students = students_by_rarity[result]
            all_weights = [rates[result] / len(students_by_rarity[result])] * len(students_by_rarity[result])


        drawn_characters.extend(random.choices(all_students, all_weights))

    print(counter)

    return drawn_characters
