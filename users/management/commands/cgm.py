from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    """Команда для заполнения групп с настроенными правами"""

    def handle(self, *args, **options):
        # Создаем новую группу «Менеджеры»
        managers = Group.objects.create(name="Менеджеры")
        # Получаем разрешения
        view_mailinglist_permission = Permission.objects.get(codename="view_mailinglist")
        view_recipient_permission = Permission.objects.get(codename="view_recipient")
        can_block_user_permission = Permission.objects.get(codename="can_block_user")
        can_mailinglist_cancel_permission = Permission.objects.get(codename="can_mailinglist_cancel")

        # Назначаем разрешения группе
        managers.permissions.add(
            view_mailinglist_permission,
            view_recipient_permission,
            can_block_user_permission,
            can_mailinglist_cancel_permission,
        )
        # Создаем пользователя
        user = CustomUser.objects.create(email="manager@mail.ru")
        user.set_password("12345")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = False
        user.save()
        # Добавляем пользователя в группу «Менеджеры»
        user.groups.add(managers)
