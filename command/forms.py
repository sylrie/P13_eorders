from django import forms

class JoinTable(forms.Form):
    table = forms.CharField(label='taken_table')
    code = forms.CharField(label='code', max_length='5')

class NewOrder(forms.Form):
    pass