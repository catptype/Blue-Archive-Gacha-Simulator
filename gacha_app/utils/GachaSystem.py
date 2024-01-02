import random
from django.contrib.auth import get_user_model

from ..models import GachaTransaction
from student_app.models import Student

class GachaSystem:
    def __init__(self, user, banner):
        self.user = user
        self.banner = banner
        self.pickup_rate = 1.0
        self.draw_rates = {
            3: float(banner.r3_rate), 
            2: float(banner.r2_rate), 
            1: float(banner.r1_rate),
        }
        self.guarantee_rarity = {
            3: self.init_guarantee_rarity(3),
            2: self.init_guarantee_rarity(2),
        }
        
    def draw_gacha(self, num_draw):
        students_pickup = list(self.banner.is_pickup.all())
        students_not_pickup = {
            3: list(self.banner.not_pickup.filter(rarity=3)),
            2: list(self.banner.not_pickup.filter(rarity=2)),
            1: list(self.banner.not_pickup.filter(rarity=1)),
        }

        drawn_students = []

        for _ in range(num_draw):
            # Update draw_rates before drawing gacha
            if self.guarantee_rarity[3] == 0:
                self.set_draw_rates(3)
            elif self.guarantee_rarity[2] == 0:
                self.set_draw_rates(2)

            drawn_rarity = random.choices(list(self.draw_rates.keys()), list(self.draw_rates.values()))[0]
            num_not_pickup = len(students_not_pickup[drawn_rarity])

            if drawn_rarity == 3 and students_pickup:
                num_pickup = len(students_pickup)             
                all_students = students_pickup + students_not_pickup[drawn_rarity]
                pickup_rates = [self.pickup_rate / num_pickup] * num_pickup
                not_pickup_rates = [(self.draw_rates[drawn_rarity] - self.pickup_rate) / num_not_pickup] * num_not_pickup
                all_rates = pickup_rates + not_pickup_rates
            else:
                all_students = students_not_pickup[drawn_rarity]
                all_rates = [self.draw_rates[drawn_rarity] / num_not_pickup] * num_not_pickup

            drawn_students.extend(random.choices(all_students, all_rates))

            # Update draw_rates after drawing gacha
            if self.guarantee_rarity[3] == 0 or self.guarantee_rarity[2] == 0:
                self.set_draw_rates(0)

            # Update guarantee countdown
            self.update_guarantee_rarity(drawn_rarity)
            
        return drawn_students
    
    def init_guarantee_rarity(self, rarity):
        if not self.user.is_authenticated and rarity == 3:
            return 199
        elif not self.user.is_authenticated and rarity == 2:
            return 9

        user_instance = get_user_model().objects.get(username=self.user.username)
        num_query = 10 if rarity == 2 else 200
        queryset = GachaTransaction.objects.filter(user=user_instance).order_by('-id')[:num_query]

        for idx, transaction in enumerate(queryset, start=1):
            if transaction.student.rarity == rarity:
                return num_query - idx

        return max(num_query - 1 - len(queryset), 0)
    
    def update_guarantee_rarity(self, drawn_rarity):
        if drawn_rarity == 3:
            self.guarantee_rarity.update({
                3: 199,
                2: max(0, self.guarantee_rarity[2] - 1),
            })
        elif drawn_rarity == 2:
            self.guarantee_rarity.update({
                3: max(0, self.guarantee_rarity[3] - 1),
                2: 9,
            })
        else:
            self.guarantee_rarity.update({
                3: max(0, self.guarantee_rarity[3] - 1),
                2: max(0, self.guarantee_rarity[2] - 1),
            })

    def save_transaction(self, drawn_students):
        if self.user.is_authenticated:
            user_instance = get_user_model().objects.get(username=self.user.username)

            # Create a list of GachaTransaction instances
            transactions = [
                GachaTransaction(
                    user=user_instance,
                    banner=self.banner,
                    student=Student.objects.get(id=student_instance.id),
                )
                for student_instance in drawn_students
            ]
            
            # Use bulk_create to insert all the records at once
            GachaTransaction.objects.bulk_create(transactions)
        else:
            pass

    def set_draw_rates(self, preset=0):
        if preset == 0: # Default
            self.draw_rates.update({
                3: float(self.banner.r3_rate), 
                2: float(self.banner.r2_rate), 
                1: float(self.banner.r1_rate),
            })
        elif preset == 2: # Guarantee Rarity = 2
            self.draw_rates.update({
                3: float(self.banner.r3_rate), 
                2: float(self.banner.r2_rate + self.banner.r1_rate), 
                1: 0.0,
            })
        elif preset == 3: # Guarantee Rarity = 2
            self.draw_rates.update({
                3: 100.0, 
                2: 0.0, 
                1: 0.0,
            })
        else:
            raise ValueError("Mode can be 0, 2, and 3")

