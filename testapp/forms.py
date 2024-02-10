from django import forms
from .models import blacklist
class SearchForm(forms.Form):

    dropdown_field = forms.ModelChoiceField(queryset=blacklist.objects.all(), empty_label='Select an option', widget=forms.Select(attrs={'class': 'form-control'}))

class YourForm(forms.Form):
    dropdown_choices = [
        ('category', 'transaction id'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
]

    dropdown_field = forms.ChoiceField(choices=dropdown_choices, widget=forms.Select(attrs={'class': 'form-control'}))