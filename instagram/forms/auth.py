from django import forms

class SignUpForm(forms.Form):
    first_name = forms.CharField(label = "First Name", max_length = 75, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label="Last Name", max_length=75, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(label = "Email", max_length=75, widget=forms.TextInput(attrs={'placeholder': "example@email.com"}))
    username = forms.CharField(label="User Name", max_length=75, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=75)
    password = forms.CharField(widget = forms.PasswordInput)
