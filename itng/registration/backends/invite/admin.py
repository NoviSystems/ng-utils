
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import get_user_model

from . import views


class AdminInvitationView(views.InvitationView):
    template_name = 'admin/registration_invite.html'

    def get_context_data(self, **kwargs):
        form = self.get_form()

        context = super(AdminInvitationView, self).get_context_data(**kwargs)
        context['opts'] = get_user_model()._meta
        context['adminform'] = admin.helpers.AdminForm(
            form, [(None, {'fields': [field.name for field in form]})], {},
        )
        return context


class UserInvitationAdmin(admin.ModelAdmin):

    def get_invite_form(self):
        return self.add_form

    def get_urls(self):
        return [
            url(
                r'^invite/$',
                self.admin_site.admin_view(
                    AdminInvitationView.as_view(form_class=self.get_invite_form())),
                name='registration_invite'),
        ] + super(UserInvitationAdmin, self).get_urls()
