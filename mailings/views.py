from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.services import get_is_manager

from .models import Attempt, MailingList, Message, Recipient
from .services import send_mailinglist


# =================== Представление «Главная страница» ===============================================================
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        owner = self.request.user
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = MailingList.objects.filter(owner=owner).count()
        context["active_mailings"] = MailingList.objects.filter(status="started", owner=owner).count()
        context["total_attempts"] = Attempt.objects.filter(mailing_list__owner=owner).count()
        context["success_attempts"] = Attempt.objects.filter(result="successful", mailing_list__owner=owner).count()
        context["failed_attempts"] = Attempt.objects.filter(result="failed", mailing_list__owner=owner).count()
        context["unique_recipients"] = Recipient.objects.filter(owner=owner).distinct().count()
        return context


# =================== Представление «Получатель рассылки» ============================================================
class RecipientListView(LoginRequiredMixin, ListView):
    """Список получателей рассылки"""

    model = Recipient
    template_name = "mailings/recipient/recipient_list.html"

    # Метод переопределения исходного набора данных
    def get_queryset(self):
        queryset = cache.get("recipient_queryset")
        if not queryset:
            queryset = super().get_queryset()
            if not get_is_manager(self.request.user, "Менеджеры"):
                queryset = queryset.filter(owner=self.request.user)
            cache.set("recipient_queryset", queryset, 60 * 15)
        return queryset


class RecipientCreateView(LoginRequiredMixin, CreateView):
    """Создание нового получателя рассылки"""

    model = Recipient
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("mailings:recipient_list")
    template_name = "mailings/recipient/recipient_form.html"

    # Метод корректности введённых данных формы
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о получателе рассылки"""

    model = Recipient
    template_name = "mailings/recipient/recipient_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not get_is_manager(self.request.user, "Менеджеры") and obj.owner != self.request.user:
            raise Http404("Доступ запрещён.")
        return obj


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление получателя рассылки"""

    model = Recipient
    fields = ["full_name", "email", "comment"]
    template_name = "mailings/recipient/recipient_form.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("Доступ запрещён.")
        return obj

    def get_success_url(self):
        """Редирект на детали получателя рассылки"""
        return reverse_lazy("mailings:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление получателя рассылки"""

    model = Recipient
    success_url = reverse_lazy("mailings:recipient_list")
    template_name = "mailings/recipient/recipient_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("Доступ запрещён.")
        return obj


# =================== Представление «Сообщение» ======================================================================
class MessageListView(LoginRequiredMixin, ListView):
    """Список сообщений"""

    model = Message
    template_name = "mailings/message/message_list.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создать новое сообщение"""

    model = Message
    fields = ["subject", "letter_body"]
    success_url = reverse_lazy("mailings:message_list")
    template_name = "mailings/message/message_form.html"


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о сообщении"""

    model = Message
    template_name = "mailings/message/message_detail.html"


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление сообщения"""

    model = Message
    fields = ["subject", "letter_body"]
    template_name = "mailings/message/message_form.html"

    def get_success_url(self):
        """Редирект на детали сообщения"""
        return reverse_lazy("mailings:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения"""

    model = Message
    success_url = reverse_lazy("mailings:message_list")
    template_name = "mailings/message/message_confirm_delete.html"


# =================== Представление «Рассылки» ======================================================================
class MailingListListView(LoginRequiredMixin, ListView):
    """Список рассылок"""

    model = MailingList
    template_name = "mailings/mailinglist/mailinglist_list.html"

    def get_queryset(self):
        queryset = cache.get("mailinglist_queryset")
        if not queryset:
            queryset = super().get_queryset()
            if not get_is_manager(self.request.user, "Менеджеры"):
                queryset = queryset.filter(owner=self.request.user)
            cache.set("mailinglist_queryset", queryset, 60 * 15)
        return queryset


class MailingListCreateView(LoginRequiredMixin, CreateView):
    """Создание новой рассылки"""

    model = MailingList
    fields = ["start_time", "end_time", "status", "message", "recipients"]
    success_url = reverse_lazy("mailings:mailinglist_list")
    template_name = "mailings/mailinglist/mailinglist_form.html"

    # Метод корректности введённых данных формы
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingListDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о рассылке"""

    model = MailingList
    template_name = "mailings/mailinglist/mailinglist_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not get_is_manager(self.request.user, "Менеджеры") and obj.owner != self.request.user:
            raise Http404("Доступ запрещён.")
        return obj

    # Метод установки дополнительного контекста
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = get_is_manager(self.request.user, "Менеджеры")
        return context


class MailingListUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление рассылки"""

    model = MailingList
    fields = ["start_time", "end_time", "status", "message", "recipients"]
    template_name = "mailings/mailinglist/mailinglist_form.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("Доступ запрещён.")
        return obj

    def get_success_url(self):
        """Редирект на детали рассылки"""
        return reverse_lazy("mailings:mailinglist_detail", kwargs={"pk": self.object.pk})


class MailingListDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление рассылки"""

    model = MailingList
    success_url = reverse_lazy("mailings:mailinglist_list")
    template_name = "mailings/mailinglist/mailinglist_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("Доступ запрещён.")
        return obj


class MailingListSendingView(LoginRequiredMixin, View):
    template_name = "newsletters/send_newsletter.html"
    success_url = reverse_lazy("mailings:mailinglist_list")

    def get(self, request, pk):
        mailinglist = get_object_or_404(MailingList, pk=pk, owner=request.user)
        if mailinglist.owner != self.request.user:
            raise Http404("Доступ запрещён.")

        send_mailinglist(mailinglist.pk)
        return HttpResponseRedirect(reverse_lazy("mailings:mailinglist_list"))


# =================== Представление «Попытка рассылки» ===============================================================
class AttemptListView(LoginRequiredMixin, ListView):
    """Список попыток рассылок"""

    model = Attempt
    template_name = "mailings/attempt/attempt_list.html"

    def get_queryset(self):
        queryset = cache.get("attempt_queryset")
        if not queryset:
            queryset = super().get_queryset()
            if not get_is_manager(self.request.user, "Менеджеры"):
                queryset = queryset.filter(mailing_list__owner=self.request.user)
            cache.set("attempt_queryset", queryset, 60 * 15)
        return queryset


class AttemptCreateView(LoginRequiredMixin, CreateView):
    """Создание новой попытки рассылки"""

    model = Attempt
    fields = ["result", "server_response", "mailing_list"]
    success_url = reverse_lazy("mailings:attempt_list")
    template_name = "mailings/attempt/attempt_form.html"


class AttemptDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о попытке рассылки"""

    model = Attempt
    template_name = "mailings/attempt/attempt_detail.html"


class AttemptUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление попытки рассылки"""

    model = Attempt
    fields = ["result", "server_response", "mailing_list"]
    template_name = "mailings/attempt/attempt_form.html"

    def get_success_url(self):
        """Редирект на детали попытки рассылки"""
        return reverse_lazy("mailings:attempt_detail", kwargs={"pk": self.object.pk})


class AttemptDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление попытки рассылки"""

    model = Attempt
    success_url = reverse_lazy("mailings:attempt_list")
    template_name = "mailings/attempt/attempt_confirm_delete.html"
