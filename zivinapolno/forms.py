from django import forms
from pro.models import UserProfile


class RegistrationForm(forms.ModelForm):
    subscribed = forms.BooleanField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'username', 'address', 'city', 'post', 'subscribed', 'password')
