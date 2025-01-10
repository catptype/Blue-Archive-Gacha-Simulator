from django.urls import path
from . import views

urlpatterns = [
    path('', views.student, name="student"),

    path('image/school/<int:school_id>', views.serve_school_image, name='serve_school_image'),
    path('image/student/<int:student_id>', views.serve_student_image, name='serve_student_image'),
]