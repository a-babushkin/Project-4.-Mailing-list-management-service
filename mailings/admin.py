from django.contrib import admin

from .models import Attempt, MailingList, Message, Recipient

admin.site.register(Recipient)
admin.site.register(Message)
admin.site.register(MailingList)
admin.site.register(Attempt)
