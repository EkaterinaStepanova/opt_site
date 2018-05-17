from django import forms
from calcs.models import Measure

class MeasureForm(forms.ModelForm):
    #method = forms.ChoiceField(widget=forms.RadioSelect, choices=Measure.METHOD_CHOICES)
    class Meta:
        model = Measure
        fields = ['name', 'bottom_border', 'upper_border', 'r', 'epsilon']