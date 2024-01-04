from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailTokenGeneration
class LoginForm(forms.Form):
   email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
   password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError("This email address is already in use.")
        return cleaned_data
    def save(self,commit=True):
        user=super().save(commit=False)
        if commit:
            user.is_active=False
            user.save()
            token=EmailTokenGeneration.objects.create(user=user)
            email_confirmation(user,token)
        return user
def email_confirmation(user,email_token):
    subject="Confirm Your Email"
    message=render_to_string('store/email_confirm.html',{
        'user':user,
        'confirm_url':f'http://merobook.onrender.com//confirm-email/{email_token}/'
    })
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    send_mail(subject,message,from_email,[to_email],fail_silently=False)
class OTPform(forms.Form):
    otpvalue=forms.CharField(label='Enter OTP',widget=forms.TextInput(attrs={'class':'form-control'}))