from attr import field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from matplotlib import ticker


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']
        
        
class TickerForm(forms.Form):
    predict = forms.CharField(label='Predict', max_length=5)