from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Imię', widget=forms.TextInput(attrs={'autocomplete': 'given-name'}))
    last_name = forms.CharField(label='Nazwisko', widget=forms.TextInput(attrs={'autocomplete': 'family-name'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    password_check = forms.CharField(label='Hasło',
                                     widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_password_check(self):
        password = self.cleaned_data.get('password_check')
        if not self.instance.check_password(password):
            raise forms.ValidationError('Podane hasło jest nieprawidłowe.')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Stare hasło', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Nowe hasło', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Potwierdź nowe hasło', widget=forms.PasswordInput)
