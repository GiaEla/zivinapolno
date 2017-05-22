from django import forms
from pro.models import UserProfile

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'username' 'address', 'city', 'post', 'subscribed')
