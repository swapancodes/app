from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CustomerRegistrationForm(UserCreationForm):
   username=forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
   password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
   password2=forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
   email=forms.CharField(required=True, label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
   class Meta:
     model=User
     fields=['username','email','password1','password2']

from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password=forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

from .models import Customer
class CustomerProfileForm(forms.ModelForm):
   class Meta:
      model=Customer
      fields=['name','locality','city','zipcode','state']
      widgets={'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}),
      'city':forms.TextInput(attrs={'class':'form-control'}),'zipcode':forms.TextInput(attrs={'class':'form-control'}),
      'state':forms.TextInput(attrs={'class':'form-control'})
      }