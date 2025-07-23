from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from config import settings
from .forms import CustomAuthenticationForm, CustomUserCreationForm, ProfileForm
from .models import CustomUser
from .services import get_is_manager


class UserListView(LoginRequiredMixin, ListView):
    """Список пользователей"""

    model = CustomUser
    permission_required = "users.can_block_user"

    # Метод переопределения исходного набора данных
    def get_queryset(self):
        queryset = cache.get("users_queryset")
        if not queryset:
            managers = Group.objects.get(name="Менеджеры")
            queryset = super().get_queryset().exclude(is_superuser=True).exclude(groups__in=[managers])
            cache.set("users_queryset", queryset, 60 * 15)  # Кешируем данные на 15 минут

        return queryset

    # Метод установки дополнительного контекста
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = get_is_manager(self.request.user, "Менеджеры")
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    """Просмотр пользователей"""

    model = CustomUser


class RegisterView(CreateView):
    """Класс для регистрации нового пользователя"""

    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    # Метод отправки письма после валидации формы
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    # Метод отправки приветственного письма
    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать в наш сервис"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        recipient_list = [user_email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, recipient_list)


class CustomLoginView(LoginView):
    """Класс входа пользователя в систему"""

    form_class = CustomAuthenticationForm
    template_name = "users/login.html"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Класс обновления пользователя (Profile)"""

    model = CustomUser
    form_class = ProfileForm
    template_name = "users/profile_form.html"
    success_url = reverse_lazy("users:users_list")
