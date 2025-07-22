from django.urls import path

from users.services import mailinglist_cancel

from .apps import MailingsConfig
from .views import (
    AttemptCreateView,
    AttemptDeleteView,
    AttemptDetailView,
    AttemptListView,
    AttemptUpdateView,
    MailingListCreateView,
    MailingListDeleteView,
    MailingListDetailView,
    MailingListListView,
    MailingListSendingView,
    MailingListUpdateView,
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
    RecipientCreateView,
    RecipientDeleteView,
    RecipientDetailView,
    RecipientListView,
    RecipientUpdateView,
)

app_name = MailingsConfig.name

urlpatterns = [
    path("recipient/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/<int:pk>/edit/", RecipientUpdateView.as_view(), name="recipient_edit"),
    path("recipient/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_edit"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailinglist/<int:pk>/send", MailingListSendingView.as_view(), name="mailinglist_send"),
    path("mailinglist/", MailingListListView.as_view(), name="mailinglist_list"),
    path("mailinglist/<int:pk>/", MailingListDetailView.as_view(), name="mailinglist_detail"),
    path("mailinglist/create/", MailingListCreateView.as_view(), name="mailinglist_create"),
    path("mailinglist/<int:pk>/edit/", MailingListUpdateView.as_view(), name="mailinglist_edit"),
    path("mailinglist/<int:pk>/delete/", MailingListDeleteView.as_view(), name="mailinglist_delete"),
    path("mailinglist/<int:pk>/cancel/", mailinglist_cancel, name="mailinglist_cancel"),
    path("attempt/", AttemptListView.as_view(), name="attempt_list"),
    path("attempt/<int:pk>/", AttemptDetailView.as_view(), name="attempt_detail"),
    path("attempt/create/", AttemptCreateView.as_view(), name="attempt_create"),
    path("attempt/<int:pk>/edit/", AttemptUpdateView.as_view(), name="attempt_edit"),
    path("attempt/<int:pk>/delete/", AttemptDeleteView.as_view(), name="attempt_delete"),
]
