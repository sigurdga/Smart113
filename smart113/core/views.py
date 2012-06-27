from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from smart113.core.models import UserProfile

class ProfileDetailView(DetailView):
    model = UserProfile

    def get_object(self):
        return self.request.user.profile

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDetailView, self).dispatch(*args, **kwargs)

class ProfilePhysicalDetailView(ProfileDetailView):
    template_name = "core/userprofile_physical_detail.html"


class ProfileKeyDetailView(ProfileDetailView):
    template_name = "core/userprofile_key_detail.html"

