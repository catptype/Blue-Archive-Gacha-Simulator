from django.urls import path
from . import views

urlpatterns = [
    path('', views.gacha, name="gacha"),
    path('<int:gacha_id>', views.gacha_detail, name="gacha_detail"),
    path('<int:gacha_id>/result', views.gacha_result, name="gacha_result"),
]
