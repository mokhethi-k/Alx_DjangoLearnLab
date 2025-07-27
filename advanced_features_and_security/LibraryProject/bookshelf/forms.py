from django import forms

class ExampleForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
