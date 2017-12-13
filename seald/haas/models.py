from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Statistics(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    algorithm = models.CharField(max_length=16)
    data = models.CharField(max_length=1048575)
    iterations = models.IntegerField()

    class Meta:
        ordering = ('created',)
