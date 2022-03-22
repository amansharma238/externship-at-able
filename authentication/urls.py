from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("remark/", views.remarkLead, name="remark"),
    path("analytics/", views.analytics, name="analytics"),
    path("", views.home, name="home"),
]

urlpatterns += staticfiles_urlpatterns()
