"""
URL configuration for chat_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin

from . import settings
from django.urls import path, include
from utils.custom_error_handlers import custom_handler_404
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login-register/',include('login_register.urls'))
    ,path('users/',include('user_module.urls')),path('groups&messages/',include('groups_and_messages.urls'))
    ,path('',include('groups_and_messages.urls'))

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
handler404=custom_handler_404
