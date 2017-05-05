
from django.conf import settings


def debug(request):
    return {
        'debug': getattr(settings, 'DEBUG', False)
    }


def testing(request):
    return {
        'testing': getattr(settings, 'TESTING', False)
    }
