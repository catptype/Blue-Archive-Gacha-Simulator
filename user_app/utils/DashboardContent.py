from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseForbidden
from django.utils.html import format_html
from django.contrib.auth import logout
from ..forms import ChangePasswordForm, ResetAccountForm, DeleteAccountForm
from gacha_app.models import GachaTransaction
from student_app.models import Student
from ..models import ObtainedStudent, ObtainedAchievement

from collections import Counter


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

        rarity_counter = {
            'r1': r1_transactions.count(),
            'r2': r2_transactions.count(),
            'r3': r3_transactions.count(),
        }

        # top3_students = {
        #     'r1': Counter(rarity_counter['r1']).most_common(3),
        #     'r2': Counter(rarity_counter['r2']).most_common(3),
        #     'r3': Counter(rarity_counter['r3']).most_common(3),
        # }

        # print("TOP3")
        # print(top3_students['r1'])
        
        context = {
            'first_r3_student': r3_transactions.first(),
            'rarity_counter': rarity_counter,
            'total_draw': sum(rarity_counter.values()),
        }
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
    
