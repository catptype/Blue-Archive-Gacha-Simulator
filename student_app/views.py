from django.shortcuts import render, redirect

# Create your views here.
from .forms import StudentForm

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gacha')
    else:
        form = StudentForm()
    context = {'form': form}
    return render(request, 'student_app/add_student.html', context)