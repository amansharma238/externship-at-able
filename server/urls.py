"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import Http404
from django.urls import path, include
from django.conf.urls import handler404
from functools import wraps


def staff_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return func(request, *args, **kwargs)
        raise Http404()
    return wrapper


admin.site.login = staff_required(admin.site.login)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("authentication.urls")),
]

handler404 = "authentication.views.error_404_view"
