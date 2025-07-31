from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from mailings.models import MailingList
from users.models import CustomUser


# Блокировка пользователя
def block_user(request, pk):
    if not request.user.has_perm("users.can_block_user"):
        messages.error(request, "У вас нет прав для блокировки пользователя")
        return redirect("users:users_list")

    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = False
    user.save()

    return redirect("users:users_list")


# Проверка вхождения пользователя в группу
def get_is_manager(user, group_name):
    return user.groups.filter(name=group_name).exists()


# Отключение рассылки
def mailinglist_cancel(request, pk):
    if not request.user.has_perm("users.can_mailinglist_cancel"):
        messages.error(request, "У вас нет прав для отключения рассылки")
        return redirect("mailings:mailinglist_list")

    mailinglist = get_object_or_404(MailingList, pk=pk)
    mailinglist.status = "completed"
    mailinglist.save()

    return redirect("mailings:mailinglist_list")
