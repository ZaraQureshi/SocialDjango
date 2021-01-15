from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate
from account.models import Account

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(max_length=60,help_text='Required.Add a valid email address')

    class Meta:
        model=Account
        fields=('email','username','password1','password2')

class AccountAuthentication(forms.ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    class Meta:
        model=Account
        fields=('email','password')

        def clean(self):
            if self.is_valid:
                email=self.cleaned_data.get('email')
                password=self.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
            #     if not user:
            #         raise forms.ValidationError("Invalid Login")
            # return self.cleaned_data

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('email','username')

        def clean_email(self):
            if self.is_valid:
                email=self.cleaned_data['email']
                try:
                    account=Account.objects.filter(pk=self.instance.pk).get(email=email)
                except Account.DoesNotExist:
                    return email
                raise forms.ValidationError("Email '%s' is already in use" %account.email)

        def clean_username(self):
            if self.is_valid:
                username=self.cleaned_data['username']
                try:
                    account=Account.objects.filter(pk=self.instance.pk).get(username=username)
                except Account.DoesNotExist:
                    return username
                raise forms.ValidationError("Username '%s' is already in use" %account.username)
