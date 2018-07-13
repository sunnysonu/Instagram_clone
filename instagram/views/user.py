from django.contrib.auth.mixins import *
from django.views.generic import *
from django.shortcuts import *
from django import urls
from instagram.forms.user import *
from instagram.models import *
from django.db.models import Q

class UserProfileView(LoginRequiredMixin, ListView):
    login_url = "instagram:login"
    model = UserProfile
    context_object_name = "profile"
    template_name = "user_profile_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context["profile"] = self.model.objects.get(user_id = self.kwargs["user_id"])
        if self.kwargs["user_id"] == self.request.user.id:
            context["is_authenticated_user"] = True
        else:
            context["is_authenticated_user"] = False
            if Followers.objects.filter(Q(follower_id=self.request.user.id) & Q(following_id=self.kwargs["user_id"])):
                context["is_following"] = True
            else:
                context["is_following"] = False
        context["posts"] = Posts.objects.filter(user_profile__id = self.kwargs["user_id"])
        return context

class OtherUserProfileView(LoginRequiredMixin, ListView):
    login_url = "instagram:login"
    model = UserProfile
    context_object_name = "profile"
    template_name = "other_user_profile_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OtherUserProfileView, self).get_context_data(**kwargs)
        context["profile"] = self.model.objects.get(user_id = self.kwargs["user_id"])
        context["posts"] = Posts.objects.filter(user_profile__id = self.kwargs["user_id"])
        return context

class CreateUserProfileView(LoginRequiredMixin, CreateView):
    login_url = "instagram:login"
    template_name = "edit_profile_template.html"
    model = UserProfile
    form_class = EditUserProfileForm

    def post(self, request, *args, **kwargs):
        form = EditUserProfileForm(request.POST, request.FILES)
        if(form.is_valid()):
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("instagram:homepage")

class EditUserProfileView(LoginRequiredMixin, UpdateView):
    login_url = "instagram:login"
    template_name = "edit_profile_template.html"
    model = UserProfile
    form_class = EditUserProfileForm
    success_url = urls.reverse_lazy("instagram:homepage")
