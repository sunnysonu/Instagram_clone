from django.urls import path
from instagram.views.auth import *
from instagram.views.user import *
from instagram.views.posts import *
from instagram.views.followers import *
from instagram.views.all_users import *

app_name = "instagram"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", Logout_user, name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user/<int:user_id>/",UserProfileView.as_view(), name = "userdetailprofile"),
    path("otheruser/<int:user_id>/", OtherUserProfileView.as_view(), name = "otheruser"),
    path("edit/<int:pk>/",EditUserProfileView.as_view(), name = "edituserprofile"),
    path("homepage/", HomePagePostsView.as_view(), name = "homepage"),
    path("createprofile/<int:pk>/", CreateUserProfileView.as_view(), name = "createprofile"),
    path("addpost/<int:pk>/", CreatePostsView.as_view(), name = "addpost"),
    path("<int:user_id>/followers/", FollowersView.as_view(), name = "followers"),
    path("<int:user_id>/following/", FollowingView.as_view(), name="following"),
    path("like/", LikeView, name = "like"),
    path("follow/", FollowView, name = "follow"),
    path("allusers/", AllUsers.as_view(), name = "all_users"),
]