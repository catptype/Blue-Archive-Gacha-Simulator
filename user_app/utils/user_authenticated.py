from functools import wraps
from django.http import HttpResponseForbidden

def user_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('HTTP403: You do not have permission to access this page.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view