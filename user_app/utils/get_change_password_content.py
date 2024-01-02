from django.template.loader import render_to_string

def get_change_password_content(request):

    context = {}
    
    html_content = render_to_string('user_app/change_password.html', context)

    return html_content