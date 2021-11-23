"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from litreview.views import tickets, security, default, subscriptions

urlpatterns = [
    path("", default.home, name="home"),
    path("sign-in", security.sign_in, name="sign_in"),
    path("sign-up", security.sign_up, name="sign_up"),
    path("subscriptions", subscriptions.subscriptions, name="subscriptions"),
    path("unsubscribe/<int:followed_user>", subscriptions.unsubscribe, name="unsubscribe"),
    path("tickets/create", tickets.create, name="ticket_create"),
    path("tickets/read/<int:id>", tickets.read, name="ticket_update"),
    path("tickets/update/<int:id>", tickets.update, name="ticket_update"),
    path("tickets.delete/<int:id>", tickets.delete, name="ticket_delete"),
    path("admin/", admin.site.urls),
]
