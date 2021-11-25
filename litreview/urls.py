from django.contrib import admin
from django.urls import path

from litreview.views import tickets, security, default, subscriptions, reviews

urlpatterns = [
    path("", default.home, name="home"),
    path("profile", default.profile, name="profile"),
    path("sign-in", security.sign_in, name="sign_in"),
    path("sign-up", security.sign_up, name="sign_up"),
    path("subscriptions", subscriptions.subscriptions, name="subscriptions"),
    path("unsubscribe/<int:followed_user>", subscriptions.unsubscribe, name="unsubscribe"),
    path("tickets/create", tickets.create, name="ticket_create"),
    path("tickets/update/<int:id>", tickets.update, name="ticket_update"),
    path("tickets/delete/<int:id>", tickets.delete, name="ticket_delete"),
    path("reviews/create/<int:ticket_id>", reviews.create, name="reviews_create"),
    path("reviews/create", reviews.create, name="reviews_create_without_ticket"),
    path("admin/", admin.site.urls),
]
