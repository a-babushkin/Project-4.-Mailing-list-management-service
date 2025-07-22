import logging
import os

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from config import settings
from mailings.models import Attempt, MailingList

logger = logging.getLogger(__name__)
log_file_path = os.path.join(settings.BASE_DIR, "logs", "mailing_send.log")
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Send mailings to recipients."

    def handle(self, *args, **options):
        from_email = settings.EMAIL_HOST_USER
        for mailing in MailingList.objects.filter(status="started"):
            if not mailing.end_time or mailing.start_time <= now() < mailing.end_time:
                for recipient in mailing.recipients.all():
                    try:
                        send_mail(mailing.message.subject, mailing.message.letter_body, from_email, [recipient.email])
                        Attempt.objects.create(result="successful", mailing_list_id=mailing.id)
                        logger.info(
                            f"Рассылка с идентификатором={mailing.id} для клиента: {recipient} произведена успешно."
                        )
                    except Exception as e:
                        Attempt.objects.create(result="failed", server_response=str(e), mailing_list_id=mailing.id)
                        logger.error(f"Ошибка отправки: {e}")
