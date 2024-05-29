from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Ranch(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='owned_ranchs', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='RanchMembership', related_name='ranches')

    def __str__(self):
        return self.name

class RanchMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ranch_memberships', on_delete=models.CASCADE)
    ranch = models.ForeignKey(Ranch, related_name='memberships', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'ranch')

    def __str__(self):
        return f"{self.user.username} - {self.ranch.name}"
