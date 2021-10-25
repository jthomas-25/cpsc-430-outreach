from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password")

class CreatePostForm(forms.Form):
    title = forms.CharField(label="Title")
    jobType = forms.CharField(label="Job Type")
    description = forms.CharField(label="Description")
