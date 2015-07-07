from django.db import transaction
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.views.generic import TemplateView, FormView

from itng.common.utils import reverse

from registration import signals, utils

from registration.backends.default.views import RegistrationView

from .forms import InviteForm, ActivationForm
from .models import RegistrationProfile

__all__ = (
    'InvitationView', 'InvitationCompleteView',
    'ActivationView', 'ActivationCompleteView',
)


class InvitationView(RegistrationView):
    template_name = 'registration/invitation_form.html'
    form_class = InviteForm

    def register(self, form):
        site = utils.get_site(self.request)

        new_user = form.save(commit=False)
        # using the proxy model with the invitation manager
        RegistrationProfile.objects.invite_user(new_user, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

    def get_success_url(self, user):
        return reverse('invitation_complete', self.request)


class InvitationCompleteView(TemplateView):
    template_name = 'registration/invitation_complete.html'


class BaseActivationView(object):

    def get_context_data(self, **kwargs):
        context = super(BaseActivationView, self).get_context_data(**kwargs)
        context['profile'] = self.profile
        return context

    @cached_property
    def profile(self):
        activation_key = self.kwargs.get('activation_key')
        try:
            return RegistrationProfile.objects.get(activation_key=activation_key)
        except RegistrationProfile.DoesNotExist:
            return None

    def post(self, *args, **kwargs):
        profile = self.profile
        if profile is None or profile.activation_key_expired():
            return super(BaseActivationView, self).get(*args, **kwargs)
        return super(BaseActivationView, self).post(*args, **kwargs)

    def activate(self, *args, **kwargs):
        """
        Given an activation key, look up and activate the user account corresponding to
        that key (if possible).

        After successful activation, the signal ``registration.signals.user_activated``
        will be sent, with the newly activated ``User`` as the keyword argument ``user``
        and the class of this backend as the sender.

        """
        activation_key = kwargs.get('activation_key')
        activated_user = RegistrationProfile.objects.activate_user(activation_key)
        return activated_user


class ActivationView(BaseActivationView, FormView):
    template_name = 'registration/activation_form.html'
    form_class = ActivationForm

    def get_form_kwargs(self):
        kwargs = super(ActivationView, self).get_form_kwargs()
        if self.profile:
            kwargs['instance'] = self.profile.user
        return kwargs

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
