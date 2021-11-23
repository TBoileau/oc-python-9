from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from src.models.ticket import Ticket


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(max_length=1024, validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, blank=True)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
