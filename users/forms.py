

from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from users.models import Message, Profile, Skill

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

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "username", "email", "location", "short_intro", "bio", "profile_img", "social_github", "social_twitter", "social_youtube", "social_website", "linkedin"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"
        exclude = ['owner']


    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})