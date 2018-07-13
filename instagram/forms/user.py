from django import forms
from instagram.models import *

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["id", "user", "follower", "following"]
        widgets = {
            "status": forms.Textarea(attrs={"class": "form-control"})
        }


