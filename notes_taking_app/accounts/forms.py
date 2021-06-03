from django import forms
from django.contrib.auth import authenticate
from .models import Account

class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control mb-3',
    'placeholder': 'Username',
  }))
  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control mb-3',
    'placeholder': 'Password',
  }))

  def clean(self):
    cd = super().clean()
    user = authenticate(username=cd['username'], password=cd['password'])
    if user is None:
      raise forms.ValidationError('Please enter the correct username and password. Note that both fields may be case-sensitive.')
    return cd  

class SignUpForm(forms.ModelForm):

  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'placeholder': 'Password',
  }))
  re_password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'placeholder': 'Confirm Password',
  }))

  class Meta:
    model = Account
    fields = ['username', 'email']
    widgets = {
      'username': forms.TextInput(attrs={ 
        'class': 'form-control',
        'placeholder': 'Username',
      }),
      'email': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address',
      }),
    }

  def clean_email(self):
    email = self.cleaned_data.get('email')  
    valid_email_extentions = ('.com', '.org', '.net')
    
    if "@" not in email or not email.endswith(valid_email_extentions):
      raise forms.ValidationError('Incorrect Email Format')
    return email 

  def clean_re_password(self):
    password = self.cleaned_data.get('password') 
    re_password = self.cleaned_data.get('re_password') 

    if password != re_password:
      raise forms.ValidationError("Password didn't Matched")
    return re_password  




