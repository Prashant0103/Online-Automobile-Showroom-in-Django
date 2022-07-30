from django import forms
from .models import car,contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class userform(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']  


class cform(forms.ModelForm):
    class Meta():
        model = car
        fields = '__all__'
        
class cont(forms.ModelForm):
    class Meta():
        model = contact
        fields = '__all__'
        
