from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.utils.html import format_html

from ..forms import ChangePasswordForm, ResetAccountForm, DeleteAccountForm
from ..models import ObtainedStudent, ObtainedAchievement, Achievement

from gacha_app.models import GachaTransaction
from student_app.models import Student

from django.db.models import Count

class DashboardContent:

    @staticmethod
    def history(request):
        tab = request.GET.get('tab', None)
        transaction_queryset = GachaTransaction.objects.filter(user=request.user).order_by('-id')

        page = request.GET.get('page', 1)
        paginator = Paginator(transaction_queryset, 5)

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
        all_transactions = GachaTransaction.objects.filter(user=request.user).order_by('id')
        r1_transactions = all_transactions.filter(student__rarity=1)
        r2_transactions = all_transactions.filter(student__rarity=2)
        r3_transactions = all_transactions.filter(student__rarity=3)

        transaction_count = {
            'r1': r1_transactions.count(),
            'r2': r2_transactions.count(),
            'r3': r3_transactions.count(),
        }

        most_obtain = {}

        transaction_list = [r1_transactions,r2_transactions,r3_transactions]

        for idx, transaction in enumerate(transaction_list, start=1):
            data = []
            queryset = transaction.values('student_id').annotate(count=Count('student_id')).order_by('-count')[:3]
            for student in queryset:
                top_student = Student.objects.get(id=student['student_id'])
                counter = student['count']
                data.append((top_student, counter))
            most_obtain[f'r{idx}'] = data

        context = {
            'first_r3_student': r3_transactions.first(),
            'transaction_count': transaction_count,
            'total_draw': sum(transaction_count.values()),
            'most_obtain': most_obtain,
        }
        html_content = render_to_string('user_app/dashboard_content/statistic.html', context)
        return html_content
    
    @staticmethod
    def achievement(request):
        user_instance = User.objects.get(username=request.user)
        all_achievements = Achievement.objects.all().order_by('id')
        obtained_achievements = []
        querysets = ObtainedAchievement.objects.filter(user=user_instance)
        for query in querysets:
            obtained_achievements.append(query.achievement)

        context = {
            "all_achievements": all_achievements,
            "obtained_achievements": obtained_achievements,
        }
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

                for model in [ObtainedStudent, ObtainedAchievement, GachaTransaction]:
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

        def render_form(request, form): # Declare this function for avoid redundancy code
            context = {
                'form': form,
                'csrf_token': get_token(request),
            }
            html_content = render_to_string('user_app/dashboard_content/delete_account.html', context)
            return False, html_content

        if request.user.is_superuser:
            return False, format_html('') # Superuser cannot delete account

        if request.method == 'POST':
            form = DeleteAccountForm(request.POST)
            if form.is_valid():
                username_login = User.objects.get(username=request.user)
                try:
                    username_form = User.objects.get(username=form.cleaned_data['username'])
                    if username_form != username_login:
                        form.add_error('username', 'Username does not match your current account.')
                        form.add_error(None, 'Delete account failed!')
                        return render_form(request, form)

                    logout(request)
                    username_login.delete()
                    return True, format_html('') 
                
                except User.DoesNotExist:
                    form.add_error('username', 'Username does not match your current account.')
                    form.add_error(None, 'Delete account failed!')
                    return render_form(request, form)
        else:
            form = DeleteAccountForm()
            
        return render_form(request, form)
    
