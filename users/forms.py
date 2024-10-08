from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, AuthenticationForm
from users.models import User
from django import forms


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password',)


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserRecoveryForm(StyleFormMixin, PasswordResetForm):
    class Meta:
        model = User
        fields = ('email',)