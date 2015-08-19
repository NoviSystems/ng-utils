
from ..decorators import login_exempt
from .form import MultipleFormView

__all__ = ('LoginExemptMixin', 'PublicMixin', 'MultipleFormView')


class LoginExemptMixin(object):

    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginExemptMixin, cls).as_view(**kwargs)
        return login_exempt(view)

PublicMixin = LoginExemptMixin
