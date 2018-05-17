# from django import forms
    
# class MeasureForm(forms.Form):

#     name = forms.CharField(help_text="name")
#     bottom_border = forms.FloatField(help_text="bottom_border", initial=0)
#     upper_border  = forms.FloatField(help_text="upper_border", initial=1)
#     r             = forms.FloatField(help_text="r", initial=3.4)
#     epsilon       = forms.FloatField(help_text="epsilon", initial=0.001)

from django.forms import ModelForm
from calcs.models import Measure

class MeasureForm(ModelForm):
    class Meta:
        model = Measure
        fields = ['name', 'bottom_border', 'upper_border', 'r', 'epsilon']