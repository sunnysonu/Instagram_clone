from django.contrib.auth.mixins import *
from django.views.generic import *
from django.shortcuts import *
from django import urls
from instagram.models import *
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse

class FollowersView(LoginRequiredMixin, ListView):
    login_url = "instagram:login"
    model = Followers
    context_object_name = "data"
    template_name = "followers_view_template.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super(FollowersView, self).get_context_data(**kwargs)
        followers_data = self.model.objects.filter(following_id = self.kwargs["user_id"])
        followers_ids = [data.follower_id for data in followers_data]
        # context["followers"] = UserProfile.objects.all().filter(user_id__in = followers_ids)
        followers_data = UserProfile.objects.all().filter(user_id__in = followers_ids)
        is_following = []
        for follower in followers_data:
            if(self.model.objects.filter(Q(following_id = follower.user.id) & Q(follower_id = user.id)).exists()):
                is_following.append(True)
            elif(follower.user.id == user.id):
                is_following.append(None)
            else:
                is_following.append(False)

        print(is_following)
        context["data"] = zip(followers_data, is_following)

        return context

class FollowingView(LoginRequiredMixin, ListView):
    login_url = "instagram:login"
    model = Followers
    context_object_name = "data"
    template_name = "following_view_template.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super(FollowingView, self).get_context_data(**kwargs)
        following_data = self.model.objects.filter(follower_id = self.kwargs["user_id"])
        following_ids = [data.following_id for data in following_data]
        following_data = UserProfile.objects.all().filter(user_id__in = following_ids)
        is_following = []

        for following in following_data:
            if(self.model.objects.filter(Q(following_id = following.user.id) & Q(follower_id = user.id)).exists()):
                is_following.append(True)
            elif(following.user.id == user.id):
                is_following.append(None)
            else:
                is_following.append(False)

        context["data"] = zip(following_data, is_following)
        return context

def FollowView(request):
    user = get_object_or_404(UserProfile, id = request.POST.get("id"))

    is_following = False
    if(Followers.objects.filter(Q(following_id = user.id) & Q(follower_id = request.user.id)).exists()):
        Followers.objects.filter(Q(following_id=user.id) & Q(follower_id=request.user.id)).delete()
        is_following = False
    else:
        record = Followers(following_id = user.id, follower_id = request.user.id)
        record.save()
        is_following = True

    obj = UserProfile.objects.get(user__id = user.id)
    obj.follower = Followers.objects.filter(following_id = user.id).count()
    obj.following = Followers.objects.filter(follower_id = user.id).count()
    obj.save()

    obj = UserProfile.objects.get(user__id = request.user.id)
    obj.follower = Followers.objects.filter(following_id = request.user.id).count()
    obj.following = Followers.objects.filter(follower_id = request.user.id).count()
    obj.save()

    print(obj.following, obj.follower)
    print(obj)

    context = {
        "is_following" : is_following,
        "follower" : user
    }

    if(request.is_ajax()):
        html = render_to_string("follow_section.html", context, request = request)
        return JsonResponse({"form" : html})