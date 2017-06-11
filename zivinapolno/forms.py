from django import forms
from pro.models import UserProfile, Offer, Product, ProductQuantity


class RegistrationForm(forms.ModelForm):
    subscribed = forms.BooleanField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }
        fields = ('first_name', 'last_name', 'email', 'address', 'city', 'post', 'subscribed', 'password')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'password')


class TicketForm(forms.ModelForm):
    quantities = forms.IntegerField()

    class Meta:
        model = Offer
        products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
        fields =('products', 'quantities')

