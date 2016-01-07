
from django.core import urlresolvers
from django.utils.encoding import smart_text


def import_class(path):
    """
    Import a class from a dot-delimited module path. Accepts both dot and
    colon seperators for the class portion of the path.

    ex::
        import_class('package.module.ClassName')

        or

        import_class('package.module:ClassName')
    """
    if ':' in path:
        module_path, class_name = path.split(':')
    else:
        module_path, class_name = path.rsplit('.', 1)

    module = __import__(module_path, fromlist=[class_name], level=0)
    return getattr(module, class_name)


class const_keys(dict):
    """
    dict subclass where keys are dot-accessible as their uppercased value.
    This is intended to be used with model choices/states, as constants are
    more durable to code changes than string literals.

    ex::
        class Example(models.Model):
            states = const_keys({
                'new': 'New',
            })
            state = models.CharField(choices=states, default=states.NEW, max_length=8)
            ...

        # accessible as:
        Example.states.NEW

    """
    def __init__(self, *args, **kwargs):
        super(const_keys, self).__init__(*args, **kwargs)
        for key in self:
            setattr(self, key.upper(), key)


class override_attr(object):
    def __init__(self, instance, attribute, value):
        self.instance = instance
        self.attribute = attribute
        self.value = value

    def __enter__(self):
        self.old_value = getattr(self.instance, self.attribute)
        setattr(self.instance, self.attribute, self.value)

    def __exit__(self, exc_type, exc_value, traceback):
        setattr(self.instance, self.attribute, self.old_value)


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
    from django.contrib.sites.requests import RequestSite
    from django.contrib.sites.models import Site

    if Site._meta.installed:
        return Site.objects.get_current()
    else:
        return RequestSite(request)


class ModelIterator(object):
    def __init__(self, queryset):
        self.queryset = queryset

    def __iter__(self):
        for obj in self.queryset.all():
            yield self.proc(obj)

    def __len__(self):
        return len(self.queryset)

    def proc(self, obj):
        raise NotImplementedError('This method must be implemented.')


class ModelPKIterator(ModelIterator):
    def proc(self, obj):
        return obj.pk


class ModelChoiceIterator(ModelIterator):
    def proc(self, obj):
        return (obj.pk, smart_text(obj))
