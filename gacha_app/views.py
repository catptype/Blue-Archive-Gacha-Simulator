# views.py
from django.shortcuts import render, redirect
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
    return render(request, 'gacha_app/add_student.html', context)

# Create your views here.
def gacha(request):
    return render(request, 'gacha_app/gacha.html')
