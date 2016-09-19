
from django.conf import settings
from django.contrib.auth.decorators import login_required
import re

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires users to be authenticated.

    Views can be made exempt with the approriate public/login exempt decorator or mixin.

    Views can also be made exempt by setting LOGIN_EXEMPT_URLS with a list of regexes.
    """

    def __init__(self, *args, **kwargs):
        super(LoginRequiredMiddleware, self).__init__(*args, **kwargs)
        regexes = getattr(settings, 'LOGIN_EXEMPT_URLS', ())
        self.regexes = list(map(re.compile, regexes))

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.user.is_authenticated() \
           or getattr(callback, 'login_exempt', False) \
           or self.is_exempt(request.path_info):
            return None

        return login_required(callback)(request, *callback_args, **callback_kwargs)

    def is_exempt(self, url):
        for regex in self.regexes:
            if regex.match(url):
                return True
        return False
