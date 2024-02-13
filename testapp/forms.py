from django import forms
from .models import blacklist,systemsettings
class SearchForm(forms.Form):

    dropdown_field = forms.ModelChoiceField(queryset=blacklist.objects.all(), empty_label='Select an option', widget=forms.Select(attrs={'class': 'form-control'}))

class YourForm(forms.Form):
    dropdown_choices = [
        ('category', 'transaction id'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
]

    dropdown_field = forms.ChoiceField(choices=dropdown_choices, widget=forms.Select(attrs={'class': 'form-control'}))

class SystemSettingsForm(forms.ModelForm):
    
    class Meta:
        model = systemsettings
        fields=['automate','locations','blacklist_add','report_add','enforce_blacklist']
        AUTOMATIONC = [
            ('all', 'Automate All Transaction'),
            ('location', 'automate by location')
        ]
        LOCATIONSC=[('Kiambu01'),('Kiambu02'),('Thika01'),('Thika02'),('Online')]
        
        BLACKLIST=[
                ('rejected alerts', 'add rejected alerts to the blacklist automatically'),
                ('false negatives','add false negatives to the blacklist automatically')]
        REPORT=[('auto', 'automatically generate reports from allowed transactions'),
                ('redirect','redirect the user to manually create a report after allowing a flagged transaction'),
                ('none', 'do not redirect the user or generate a report automatically')]
        automate = forms.ChoiceField(choices=AUTOMATIONC)
        locations = forms.MultipleChoiceField(choices=LOCATIONSC,widget=forms.CheckboxSelectMultiple)
        blacklist_add = forms.ChoiceField(choices=BLACKLIST)
        report_add=forms.ChoiceField(choices=REPORT)
        enforce_blacklist = forms.BooleanField(initial=False, required=False)
