
from django import forms
from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "featured_img", "demo_link","source_link","tags"]

        widgets = {
            "tags": forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        #1st way of modifying field classes
        # self.fields['title'].widget.attrs.update({'class':'input'})

        #2nd way of modifying field classes
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})