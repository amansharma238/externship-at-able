from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("analytics/", views.analytics, name="analytics"),
    path("", views.home, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# print(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
