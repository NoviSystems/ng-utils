
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password


class InviteForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (model.USERNAME_FIELD, ) + tuple(model.REQUIRED_FIELDS)


class ActivationForm(forms.ModelForm):
    """
    Form for registering a new user account.
    Subclasses should feel free to add any additional validation they
    need. Refer to ``RegistrationFormTermsOfService``,
    ``RegistrationFormUniqueEmail``, and ``RegistrationFormNoFreeEmail``.
    If you are using a custom user model, you should use/subclass the user
    creation form provided by that package, or define your own form that
    saves an instance of ``AUTH_USER_MODEL``.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification.")
    )

    class Meta:
        model = get_user_model()
        fields = ('password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return make_password(password2)

    def clean(self):
        password = make_password(self.cleaned_data.get('password1'))
        self.cleaned_data['password'] = password
        if 'password1' in self.cleaned_data:
            del self.cleaned_data['password1']
        if 'password2' in self.cleaned_data:
            del self.cleaned_data['password2']
        return self.cleaned_data
