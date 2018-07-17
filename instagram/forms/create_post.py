from django import forms
from instagram.models import *

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ["id", "user_profile", "likes"]