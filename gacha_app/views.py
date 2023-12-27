import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import GachaBanner, GachaTransaction
from student_app.models import Student

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
        elif 'draw_10' in request.POST:
            num_draw = 10
        elif 'draw_100' in request.POST:
            num_draw = 100
        else:
            raise ValueError("Invalid draw option selected")
        
        drawn_students = draw_gacha(request.user, banner, num_draw)
        # Save transaction
        if request.user.is_authenticated:
            save_gacha_records(request.user, banner, drawn_students)

        # Prepare web context
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
    
def draw_gacha(user, banner, num_draws):

    def check_remain_rarity(rarity):
        if user.is_authenticated and rarity in [2, 3]:
            user_instance = get_user_model().objects.get(username=user.username)
            num_query = 10 if rarity == 2 else 200
            queryset = GachaTransaction.objects.filter(user=user_instance).order_by('-id')[:num_query]

            for idx, transaction in enumerate(queryset, start=1):
                if transaction.student.rarity == rarity:
                    return num_query - idx

            return max(num_query - 1 - len(queryset), 0)
        else:
            return None # For guest user
    
    guarantee = {
        3: check_remain_rarity(3) if user.is_authenticated else 199,
        2: check_remain_rarity(2) if user.is_authenticated else 9,
    }
    
    pickup_rate = 1.0

    draw_rates = {
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

    drawn_students = []

    for _ in range(num_draws):
        # Override draw rate
        if guarantee[3] == 0:
            draw_rates.update({3: 100.0, 2: 0.0, 1: 0.0})
        elif guarantee[2] == 0:
            draw_rates.update({
                3: float(banner.rate_3_star),
                2: float(banner.rate_2_star + banner.rate_1_star),
                1: 0.0,
            })
        
        # Draw gacha
        drawn_rarity = random.choices(list(draw_rates.keys()), list(draw_rates.values()))[0]
        
        if drawn_rarity == 3 and banner.is_pickup.all():
            all_students = student_pickup + students_by_rarity[drawn_rarity]
            pickup_weights = [pickup_rate / len(student_pickup)] * len(student_pickup)
            not_pickup_weight = [(draw_rates[drawn_rarity] - pickup_rate) / len(students_by_rarity[drawn_rarity])] * len(students_by_rarity[drawn_rarity])
            all_weights = pickup_weights + not_pickup_weight
    
        else:
            all_students = students_by_rarity[drawn_rarity]
            all_weights = [draw_rates[drawn_rarity] / len(students_by_rarity[drawn_rarity])] * len(students_by_rarity[drawn_rarity])

        drawn_students.extend(random.choices(all_students, all_weights))
        
        # Reset draw rate to default after guarantee
        if guarantee[3] == 0 or guarantee[2] == 0:
            draw_rates.update({
                3: float(banner.rate_3_star), 
                2: float(banner.rate_2_star), 
                1: float(banner.rate_1_star),
            })
        
        # Update guarantee countdown
        if drawn_rarity == 3:
            guarantee.update({
                3: 199,
                2: max(0, guarantee[2] - 1),
            })
        elif drawn_rarity == 2:
            guarantee.update({
                3: max(0, guarantee[3] - 1),
                2: 9,
            })
        else:
            guarantee.update({
                3: max(0, guarantee[3] - 1),
                2: max(0, guarantee[2] - 1),
            })

    return drawn_students

def save_gacha_records(user, banner, drawn_students):
    user_instance = get_user_model().objects.get(username=user.username)

    # Create a list of GachaTransaction instances
    transactions = [
        GachaTransaction(
            user=user_instance,
            banner=banner,
            student=Student.objects.get(id=student_instance.id),
        )
        for student_instance in drawn_students
    ]

    # Use bulk_create to insert all the records at once
    GachaTransaction.objects.bulk_create(transactions)
