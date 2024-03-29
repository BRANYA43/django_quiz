from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import widgets

from .apps import user_register
from .validators import validate_email_exist


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='email')
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html
                                )
    password2 = forms.CharField(
        label='confirm password',
        widget=forms.PasswordInput,
        help_text='please repeat password'
    )

    def clean_password(self):
        pwd = self.cleaned_data['password1']
        if pwd:
            password_validation.validate_password(pwd)
        return pwd

    def clean(self):
        super().clean()
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError(
                {'password2': ValidationError('Password not equals', code='password_mismatch')}
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_activated = False
        user.is_active = False

        if commit:
            user.save()

        user_register.send(get_user_model(), instance=user)

        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password1',
            'password2',

        )


class UserUpdateForm(UserChangeForm):
    avatar = forms.ImageField(required=False, widget=widgets.FileInput())
    birthday = forms.DateField(required=False, widget=widgets.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birthday',
            'city',
            'avatar',
        )


class UserReactivationForm(forms.Form):
    email = forms.EmailField(required=True, validators=[validate_email_exist])

    def clean_email(self):
        model = get_user_model()
        email = self.cleaned_data['email']
        user = model.objects.get(email=email)
        user_register.send(get_user_model(), instance=user)
        return email
