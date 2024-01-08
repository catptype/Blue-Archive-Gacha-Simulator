from django.shortcuts import render
from .models import Student, School

def student(request):
    students = Student.objects.all().order_by('name')
    schools = School.objects.all().order_by('name')
    context = {
        'students': students,
        'schools': schools,
    }
    return render(request, 'student_app/student.html', context)