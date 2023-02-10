from django import forms
from .models import Contact, UserProfile1, SignUp


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile1
        fields = ['skills', 'experiences', 'hedline']
        # fields = "__all__"


class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        # fields = ['name', 'username', 'email', 'location', 'password']
        fields = "__all__"
