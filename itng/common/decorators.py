
from functools import wraps
from django.utils.decorators import available_attrs

__all__ = ('login_exempt', 'public')


def login_exempt(view_func):
    """
    Marks a view function as public, exempting users from being required to log in.
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.login_exempt = True

    return wrapped_view
public = login_exempt
