from django.template.loader import render_to_string

def get_statistic_content(request):

    context = {}
    
    html_content = render_to_string('user_app/statistic.html', context)

    return html_content