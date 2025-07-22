from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from email_validator import validate_email

from .models import CustomUser


# Форма регистрации
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email",)

    # Стилизация полей формы
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "type": "email", "placeholder": "Введите E-mail"}
        )

        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})

        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})

    # Валидатор для проверки поля email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not validate_email(email):
            raise forms.ValidationError("Неправильный формат Электронной почты.")
        return email


# Форма авторизации
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-control", "type": "email"}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
                "type": "password",
            }
        ),
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "country",
            "is_active",
        )

    # Стилизация полей формы
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "type": "email", "placeholder": "Ваш E-mail"}
        )

        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Ваше имя"})

        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Ваше фамилия"})

        self.fields["phone_number"].widget.attrs.update({"class": "form-control"})

        self.fields["avatar"].widget.attrs.update({"class": "form-control"})

        self.fields["country"].widget.attrs.update({"class": "form-control"})

        self.fields["is_active"].widget.attrs.update({"class": "form-checkbox"})
