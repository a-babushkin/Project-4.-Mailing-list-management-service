from django.db import models

from users.models import CustomUser


# =================== Модель «Получатель рассылки» ====================================================================
class Recipient(models.Model):
    """Описание модели Получатель рассылки"""

    email = models.CharField(max_length=250, verbose_name="Электронная почта", unique=True)
    full_name = models.CharField(max_length=250, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="recipient_owner",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["full_name"]


# =================== Модель «Сообщение» =============================================================================
class Message(models.Model):
    """Описание модели Сообщение"""

    subject = models.CharField(max_length=250, verbose_name="Тема письма")
    letter_body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]


# =================== Модель «Рассылка» ============================================================================
STATUS_CHOICES = [("created", "Создана"), ("started", "Запущена"), ("completed", "Завершена")]


class MailingList(models.Model):
    """Описание модели Рассылка"""

    start_time = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created", verbose_name="Статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="mailinglist_owner",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.start_time} - {self.status}: {self.message}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["start_time"]


# =================== Модель «Попытка рассылки» ======================================================================
RESULT_CHOICES = [("successful", "Успешно"), ("failed", "Не успешно")]


class Attempt(models.Model):
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, verbose_name="Статус")
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE, verbose_name="Рассылка")

    def __str__(self):
        return f"{self.attempt_time}: {self.result}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["attempt_time"]
