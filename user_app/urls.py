from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('register', views.register, name="register"),
    path('register_complete', views.register_complete, name="register_complete"),
    path('forget', views.forget, name='forget'),
    path('dashboard', views.dashboard, name='dashboard'),
]