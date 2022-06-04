
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        #1st way of modifying field classes
        # self.fields['title'].widget.attrs.update({'class':'input'})

        #2nd way of modifying field classes
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['password1'].widget.attrs.update({'placeholder': '•••••••••••••'})
        self.fields['password2'].widget.attrs.update({'placeholder': '•••••••••••••'})