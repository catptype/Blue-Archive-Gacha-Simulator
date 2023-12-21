from django.shortcuts import render
from .models import Student

def student(request):
    students = Student.objects.all().order_by('name')
    context = {
        'students': students
    }
    return render(request, 'student_app/student.html', context)