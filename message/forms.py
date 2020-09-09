from django import forms

class NewComment(forms.Form):
    message = forms.CharField(label='message')
    