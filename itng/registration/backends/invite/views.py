from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

from itng.common.utils import reverse

from registration import signals

from registration.backends.hmac.views import RegistrationView, ActivationView as BaseActivationView

from .forms import InviteForm, ActivationForm

__all__ = (
    'InvitationView', 'InvitationCompleteView',
    'ActivationView', 'ActivationCompleteView',
)


class InvitationView(RegistrationView):
    template_name = 'registration/invitation_form.html'
    form_class = InviteForm

    email_body_template = 'registration/invitation_email.txt'
    email_subject_template = 'registration/invitation_email_subject.txt'

    def get_success_url(self, user):
        return reverse('invitation_complete', self.request)

    def create_inactive_user(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.set_unusable_password()
        new_user.save()

        self.send_activation_email(new_user)

        return new_user


class InvitationCompleteView(TemplateView):
    template_name = 'registration/invitation_complete.html'


class ActivationView(BaseActivationView, FormView):
    template_name = 'registration/activation_form.html'
    form_class = ActivationForm

    def get_form_kwargs(self):
        kwargs = super(ActivationView, self).get_form_kwargs()
        username = self.validate_key(kwargs.get('activation_key'))
        if username:
            kwargs['instance'] = self.get_user(username)

        return kwargs

    def get(self, *args, **kwargs):
        return super(FormView, self).get(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        activated_user = self.activate(*self.args, **self.kwargs)
        if activated_user:
            # We need to update the activated user with the form's cleaned_data since
            # since calling form.save() will overwrite the activated user.
            activated_user.__dict__.update(form.cleaned_data)
            activated_user.save()
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=self.request)
            success_url = self.get_success_url(activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super(ActivationView, self).get(*args, **kwargs)

    def get_success_url(self, user):
        return reverse('activation_complete', self.request)


class ActivationCompleteView(TemplateView):
    template_name = 'registration/activation_complete.html'
