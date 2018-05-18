from django import forms
from calcs.models import Measure
from py_expression_eval import Parser

class MeasureForm(forms.ModelForm):
    #method = forms.ChoiceField(widget=forms.RadioSelect, choices=Measure.METHOD_CHOICES)

    def clean_function(self):
        data = self.cleaned_data['function']      
        try:
            parser = Parser()
            func = parser.parse(data)
            print(func.variables())
            if len(func.variables()) > 1:
                    raise Exception('too much variables')
        except Exception:
            raise forms.ValidationError(str(data)+' is not a function')
        return data

    class Meta:
        model = Measure
        fields = ['name', 'bottom_border', 'upper_border', 'r', 'epsilon', 'function']