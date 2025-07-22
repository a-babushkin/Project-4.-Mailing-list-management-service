from django import forms
from email_validator import validate_email

from .models import Attempt, MailingList, Message, Recipient


# =================== Форма модели «Получатель рассылки» =============================================================
class RecipientForm(forms.ModelForm):
    """Форма модели Получатель рассылки"""

    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]

    # Валидатор для проверки поля email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not validate_email(email):
            raise forms.ValidationError("Неправильный формат Электронной почты.")
        return email


# =================== Форма модели «Сообщение» =======================================================================
class MessageForm(forms.ModelForm):
    """Форма модели Сообщение"""

    class Meta:
        model = Message
        fields = ["subject", "body"]

    # Стилизация полей формы
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        # ---------- Subject -------------
        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему письма"})

        # ---------- Body -------------
        self.fields["body"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст письма"})


# =================== Форма модели «Рассылка» =======================================================================
class MailingListForm(forms.ModelForm):
    """Форма модели Рассылка"""

    class Meta:
        model = MailingList
        fields = ["start_time", "end_time", "status", "message", "recipients"]

    # Стилизация полей формы
    def __init__(self, *args, **kwargs):
        super(MailingListForm, self).__init__(*args, **kwargs)

        # ---------- Start Time -------------
        self.fields["start_time"].widget.attrs.update({"class": "form-control", "type": "date"})

        # ---------- End Time -------------
        self.fields["end_time"].widget.attrs.update({"class": "form-control", "type": "date"})

        # ---------- Status -------------
        self.fields["status"].widget.attrs.update({"class": "form-select"})

        # ---------- Message -------------
        self.fields["message"].widget.attrs.update({"class": "form-select"})

        # ---------- Recipients -------------
        self.fields["recipients"].widget.attrs.update({"class": "form-select"})

    # Валидатор для проверки соответствия дат
    def clean_end_time(self):
        end_time = self.cleaned_data.get("end_time")
        start_time = self.cleaned_data.get("start_time")
        if end_time < start_time:
            raise forms.ValidationError(
                f"Дата окончания рассылки ({end_time}) не может быть меньше начала ({start_time})"
            )
        return end_time


# =================== Форма модели «Попытка рассылки» ================================================================
class AttemptForm(forms.ModelForm):
    """Форма модели Рассылка"""

    class Meta:
        model = Attempt
        fields = ["result", "server_response", "mailing_list"]

    # Стилизация полей формы
    def __init__(self, *args, **kwargs):
        super(AttemptForm, self).__init__(*args, **kwargs)

        # ---------- Result -------------
        self.fields["result"].widget.attrs.update({"class": "form-select"})

        # ---------- Server Response -------------
        self.fields["server_response"].widget.attrs.update({"class": "form-control"})

        # ---------- Mailing List -------------
        self.fields["mailing_list"].widget.attrs.update({"class": "form-control"})
