from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from mailings.views import HomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("mailings/", include("mailings.urls", namespace="mailings")),
    path("users/", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
