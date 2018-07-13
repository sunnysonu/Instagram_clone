from django.contrib.auth.mixins import *
from django.views.generic import *
from django.shortcuts import *
from django import urls
from instagram.models import *
from instagram.forms.create_post import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q

class CreatePostsView(LoginRequiredMixin, CreateView):
    login_url = "instagram:login"
    template_name = "create_post_template.html"
    models = Posts
    form_class = CreatePostForm

    def post(self, request, *args, **kwargs):
        form = CreatePostForm(request.POST, request.FILES)
        if(form.is_valid()):
            post = form.save(commit=False)
            post.user_profile = request.user.userprofile
            post.save()
            return redirect("instagram:homepage")

class HomePagePostsView(LoginRequiredMixin, ListView):
    login_url = "instagram:login"
    model = Posts
    context_object_name = "posts"
    template_name = "home_page_posts.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super(HomePagePostsView, self).get_context_data(**kwargs)
        following_data = Followers.objects.filter(follower_id = user.id)
        following_ids = [data.following_id for data in following_data]
        posts = self.model.objects.filter(Q(user_profile__id__in=following_ids) | Q(user_profile__id = user.id))
        context["user"] = user
        likes = []
        for post in posts:
            print(post.id, len(post.likes.all()))
            if(post.likes.filter(id = user.id).exists()):
                likes.append(True)
            else:
                likes.append(False)
        context["data"] = zip(posts, likes)
        return context

def LikeView(request):
    post = get_object_or_404(Posts, id = request.POST.get("id"))
    is_liked = False
    print("Here")
    if(post.likes.filter(id = request.user.id).exists()):
        post.likes.remove(request.user)
        print(post.id)
        is_liked = False
    else:
        post.likes.add(request.user)
        print(post.id)
        is_liked = True

    context = {
        "post" : post,
        "is_liked" : is_liked
    }
    if(request.is_ajax()):
        html = render_to_string("like_section.html", context, request = request)
        return JsonResponse({"form" : html})

