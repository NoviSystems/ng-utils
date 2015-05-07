
from django.db import transaction
from registration import models


class InvitationManager(models.RegistrationManager):
    """
    Custom manager for the ``RegistrationProfile`` model.

    This manager extends the base ``RegistrationManager`` with a slightly modified
    process for inviting users.

    """

    @transaction.atomic
    def invite_user(self, user, site, send_email=True):
        """
        Invites a ``User``, by creating a ``RegistrationProfile`` that will manage their
        activation process. The password is unset and the account made inactive, as these
        values need to be set during the activation process.

        By default, an activation email containing the activation key will be sent to the
        new user. To disable this, pass ``send_email=False``.

        """
        user.is_active = False
        user.set_unusable_password()
        user.save()

        registration_profile = self.create_profile(user)

        if send_email:
            registration_profile.send_activation_email(
                site,
                subject_template_name='registration/invitation_email_subject.txt',
                text_template_name='registration/invitation_email.txt',
                html_template_name='registration/invitation_email.html',
            )

        return registration_profile


class RegistrationProfile(models.RegistrationProfile):
    """
    A proxy to the base ``RegistrationProfile`` that sets the default manager
    to the invite backend ``InvitationManager``.

    """

    objects = InvitationManager()

    # For some reason:
    # class Meta(models.RegistrationProfile.Meta):
    # AttributeError: type object 'RegistrationProfile' has no attribute 'Meta'
    # wat.
    class Meta:
        proxy = True
