from django import forms
from calcs.models import Measure
from py_expression_eval import Parser

GLOBAL_SEARCH = 'gs'
PIYAVSKY = 'pi'
METHOD_CHOICES = (
    (GLOBAL_SEARCH, 'global_search'),
    (PIYAVSKY, 'piyavsky'),
)


class MeasureForm(forms.ModelForm):

    #method = forms.ChoiceField(label='Optimization method', widget=forms.Select(choices=METHOD_CHOICES))
    #method = forms.ChoiceField(label='Optimization method', choices=METHOD_CHOICES, widget=forms.Select)

    def clean_function(self):
        data = self.cleaned_data['function']      
        try:
            parser = Parser()
            func = parser.parse(data)
            if len(func.variables()) > 1:
                    raise Exception('too much variables')
        except Exception as exc:
            raise forms.ValidationError('Error! '+str(data)+' is not correct function')
        return data

    class Meta:
        model = Measure
        fields = ['name', 'bottom_border', 'upper_border', 'r', 'epsilon', 'function', 'method']