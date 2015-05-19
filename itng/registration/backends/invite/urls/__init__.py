import itng.registration.backends.invite.urls.activation as activation
import itng.registration.backends.invite.urls.invitation as invitation

"""
Default URL conf for the ng-utils invite registration backend.

This URL conf simply includes the URLs for both invitation and activation functionality.
If the default behavior of these views is acceptable to you, simply use a line like this
in your root URLconf to set up the default URLs for registration::

    (r'^', include('itng.registration.backends.invite.urls')),

If you'd like to customize registration behavior, feel free to set up
your own URL patterns for these views instead.

"""

urlpatterns = activation.urlpatterns + invitation.urlpatterns
