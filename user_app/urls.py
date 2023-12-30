from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('register', views.register, name="register"),
    path('register_complete', views.register_complete, name="register_complete"),
    path('forget', views.forget, name='forget'),
    # After login
    path('dashboard', views.dashboard, name='dashboard'),
    # Gacha section
    path('dashboard/history', views.history, name='history'),
    path('dashboard/statistic', views.statistic, name='statistic'),
    # Account section
    path('dashboard/change_password', views.change_password, name='change_password'),
]