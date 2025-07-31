import logging
import os

from django.core.mail import send_mail
from django.utils import timezone

from config import settings

from .models import Attempt, MailingList

logger = logging.getLogger(__name__)
log_file_path = os.path.join(settings.BASE_DIR, "logs", "mailing_send.log")
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def send_mailinglist(pk):
    """Отправка рассылки по требованию"""
    mailinglist = MailingList.objects.get(pk=pk)
    now = timezone.now()
    from_email = settings.EMAIL_HOST_USER

    subject = mailinglist.message.subject
    message = mailinglist.message.letter_body

    if mailinglist.status != "started" or not (mailinglist.start_time <= now < mailinglist.end_time):
        logger.info(f"Рассылка {mailinglist.id} пока не запущена или завершила свою работу.")
    else:
        for recipient in mailinglist.recipients.all():
            if not recipient.email:
                logger.warning(f"У получателя {recipient} отсутствует действительный адрес электронной почты.")
                break
            try:
                send_mail(subject, message, from_email, [recipient.email])
                Attempt.objects.create(result="successful", mailing_list_id=mailinglist.id)
                logger.info(
                    f"Рассылка с идентификатором={mailinglist.id} для клиента: {recipient} произведена успешно."
                )

            except Exception as e:
                Attempt.objects.create(result="failed", server_response=str(e), mailing_list_id=mailinglist.id)
                logger.error(f"Ошибка отправки: {e}")
