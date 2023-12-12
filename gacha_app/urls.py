from django.urls import path
from . import views

urlpatterns = [
    path('', views.gacha, name="gacha"),
    path('add_student', views.add_student, name="add_student"),
]
