from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.utils.html import format_html
from ..forms import ChangePasswordForm, ResetAccountForm
from gacha_app.models import GachaTransaction
from student_app.models import Student
from ..models import ObtainedStudent, ObtainedAchievement

class DashboardContent:

    @staticmethod
    def history(request):
        tab = request.GET.get('tab', None)
        transactions = GachaTransaction.objects.filter(user=request.user).order_by('-id')

        page = request.GET.get('page', 1)
        paginator = Paginator(transactions, 10)

        try:
            # Get the transactions for the requested page
            transactions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            transactions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver the last page
            transactions = paginator.page(paginator.num_pages)

        context = {
            'tab': tab,
            'previous_page': int(page) - 1,
            'next_page': int(page) + 1,
            'transactions': transactions,
        }

        html_content = render_to_string('user_app/dashboard_content/history.html', context)

        return html_content

    @staticmethod
    def statistic(request):
        context = {}
        html_content = render_to_string('user_app/dashboard_content/statistic.html', context)
        return html_content
    
    @staticmethod
    def achievement(request):
        context = {}
        html_content = render_to_string('user_app/dashboard_content/achievement.html', context)
        return html_content
    
    @staticmethod
    def collection(request):
        user_instance = User.objects.get(username=request.user)
        all_students = Student.objects.all().order_by('name')
        obtained_students = []
        querysets = ObtainedStudent.objects.filter(user=user_instance)
            
        for query in querysets:
            obtained_students.append(query.student)

        context = {
            'all_students': all_students,
            'obtained_students': obtained_students,
        }
        html_content = render_to_string('user_app/dashboard_content/collection.html', context)
        return html_content
    
    @staticmethod
    def change_password(request):
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['password1']
                user_instance = User.objects.get(username=request.user)
                user_instance.set_password(new_password)
                user_instance.save()
                update_session_auth_hash(request, user_instance)
                return format_html('<h2>Change password successfully!</h2>')
        else:
            form = ChangePasswordForm()
        
        context = {
            'form': form,
            'csrf_token': get_token(request),
        }
        html_content = render_to_string('user_app/dashboard_content/change_password.html', context)
        return html_content
    
    @staticmethod
    def reset_account(request):
        if request.method == 'POST':
            form = ResetAccountForm(request.POST)
            if form.is_valid():
                user_instance = User.objects.get(username=request.user)

                for model in [ObtainedStudent, ObtainedStudent, GachaTransaction]:
                    queryset = model.objects.filter(user=user_instance)
                    queryset.delete()
                
                return format_html('<h2>Reset account successfully!</h2>')
        else:
            form = ResetAccountForm()

        context = {
            'form': form,
            'csrf_token': get_token(request),
        }
        html_content = render_to_string('user_app/dashboard_content/reset_account.html', context)
        return html_content
    
    @staticmethod
    def delete_account(request):
        context = {}
        html_content = render_to_string('user_app/dashboard_content/delete_account.html', context)
        return html_content
    
