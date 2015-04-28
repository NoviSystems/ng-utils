
from itng.common.decorators import login_exempt

__all__ = ('LoginExemptMixin', 'PublicMixin')


class LoginExemptMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginExemptMixin, cls).as_view(**initkwargs)
        return login_exempt(view)

PublicMixin = LoginExemptMixin
