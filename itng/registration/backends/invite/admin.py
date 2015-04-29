
from django.conf.urls import url
from django.contrib import admin

from . import views


class AdminInvitationView(views.InvitationView):
    template_name = 'admin/registration_invite.html'


class UserInvitationAdmin(admin.ModelAdmin):

    def get_invite_form(self):
        return self.add_form

    def get_urls(self):
        return [
            url(r'^invite/$', self.admin_site.admin_view(AdminInvitationView.as_view()), name='registration_invite'),
        ] + super(UserInvitationAdmin, self).get_urls()
