
from django.conf import settings


def auth_base(request):
    return {
        'auth_base': getattr(settings, 'REGISTRATION_AUTH_BASE', 'registration/auth/base.html')
    }
