
from django.core import urlresolvers


def relative_viewname(viewname, resolver):
    """
    """
    return ':'.join(
        filter(None, [
            resolver.app_name, resolver.namespace, viewname
        ])
    )


def reverse(viewname, request, urlconf=None, args=None, kwargs=None, current_app=None):
    """
    A wrapper around Django's builtin `django.core.urlresolvers.reverse` utility function
    that will use the current request to derive the `app_name` and `namespace`. This is
    most useful for apps that need to reverse their own URLs.
    """
    viewname = relative_viewname(viewname, request.resolver_match)
    return urlresolvers.reverse(viewname, urlconf, args, kwargs, current_app)


def get_site(request):
    from django.contrib.sites.models import RequestSite
    from django.contrib.sites.models import Site

    if Site._meta.installed:
        return Site.objects.get_current()
    else:
        return RequestSite(request)
