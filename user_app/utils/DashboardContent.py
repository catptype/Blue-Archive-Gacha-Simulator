from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string

from ..models import ObtainedAchievement, ObtainedStudent
from gacha_app.models import GachaTransaction

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
        context = {}
        html_content = render_to_string('user_app/dashboard_content/collection.html', context)
        return html_content
    
    @staticmethod
    def change_password(request):
        context = {}
        html_content = render_to_string('user_app/dashboard_content/change_password.html', context)
        return html_content