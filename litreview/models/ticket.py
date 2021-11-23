import uuid

from django.conf import settings
from django.db import models

from litreview import settings as app_settings


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=lambda instance, filename: f"{app_settings.UPLOAD_DIR}/{uuid.uuid4()}_{filename}",
    )
    time_created = models.DateTimeField(auto_now_add=True)
