from instagram.models import *
from django.views.generic import *
from django.shortcuts import *
from django.shortcuts import *
from django.contrib.auth.mixins import *
from django.db.models import Q

class AllUsers(LoginRequiredMixin, ListView):
    login_url = "instagram:login"
    model = UserProfile
    context_object_name = "data"
    template_name = "all_user_template_form.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super(AllUsers, self).get_context_data(**kwargs)
        following_data = Followers.objects.filter(follower_id = user.id)
        following_ids = [data.following_id for data in following_data]
        users = self.model.objects.all().exclude(Q(user__id__in = following_ids) | Q(user__id = user.id))

        is_following = []
        for user in users:
            is_following.append(False)

        context["data"] = zip(users, is_following)
        return context