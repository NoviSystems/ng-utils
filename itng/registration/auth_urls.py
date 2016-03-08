"""
URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up the
following patterns based at whatever URL prefix they are included
under:

* User login at ``login/``.

* User logout at ``logout/``.

* The two-step password change at ``password/change/`` and
  ``password/change/done/``.

* The four-step password reset at ``password/reset/``,
  ``password/reset/confirm/``, ``password/reset/complete/`` and
  ``password/reset/done/``.

The default registration backend already has an ``include()`` for
these URLs, so under the default setup it is not necessary to manually
include these views. Other backends may or may not include them;
consult a specific backend's documentation for details.

"""

from django.conf.urls import url
from django.contrib.auth import views

_password_reset_confirm = r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'


urlpatterns = [
    url(r'^login/$',                    views.login,                    {'template_name': 'registration/auth/login.html'},                      name='login'),                      # flake8: noqa
    url(r'^logout/$',                   views.logout,                   {'template_name': 'registration/auth/logged_out.html'},                 name='logout'),                     # flake8: noqa
    url(r'^password/change/$',          views.password_change,          {'template_name': 'registration/auth/password_change_form.html'},       name='password_change'),            # flake8: noqa
    url(r'^password/change/done/$',     views.password_change_done,     {'template_name': 'registration/auth/password_change_done.html'},       name='password_change_done'),       # flake8: noqa
    url(r'^password/reset/$',           views.password_reset,           {'template_name': 'registration/auth/password_reset_form.html'},        name='password_reset'),             # flake8: noqa
    url(_password_reset_confirm,        views.password_reset_confirm,   {'template_name': 'registration/auth/password_reset_confirm.html'},     name='password_reset_confirm'),     # flake8: noqa
    url(r'^password/reset/complete/$',  views.password_reset_complete,  {'template_name': 'registration/auth/password_reset_complete.html'},    name='password_reset_complete'),    # flake8: noqa
    url(r'^password/reset/done/$',      views.password_reset_done,      {'template_name': 'registration/auth/password_reset_done.html'},        name='password_reset_done'),        # flake8: noqa
]
