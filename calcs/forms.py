from django import forms
from calcs.models import Measure
from py_expression_eval import Parser
from django.contrib.auth.models import User

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


class UserCreateForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']  
        confirm_password = self.cleaned_data['confirm_password']  

        if User.objects.filter(username=username).exists():
            self.add_error( 'username', 'User '+str(username)+' already exist')
        else:
            if password != confirm_password:
                self.add_error( 'password', 'Passwords does not match' )

        return data

    class Meta:
        model = User
        fields = ('username','password')
        widgets = {
            'password': forms.PasswordInput(),
        }


class UserLoginForm(forms.ModelForm):

    def clean(self):  
        data = self.cleaned_data

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']  

        if not User.objects.filter(username=username).exists():
            self.add_error( 'username', 'User ' + str(username) + ' not foung. Please Sign-up')
        else:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                self.add_error( 'password', 'Not correct password.' )

        return data

    class Meta:
        model = User
        fields = ('username','password')
        widgets = {
            'password': forms.PasswordInput(),
        }