from unicodedata import name
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("leads/", views.lead_list, name="lead_list"),
    path("users/", views.user_list, name="user_list"),
    path("users/<str:email>", views.user_detail, name="user_detail"),
    path("remarks/", views.remark_list, name="remark_list"),
    path("remarks/<str:email>/<int:id>", views.remark_detail, name="remark_detail"),
]

urlpatterns += staticfiles_urlpatterns()
