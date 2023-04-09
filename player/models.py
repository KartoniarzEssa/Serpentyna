from django.db import models

# Create your models here.

class ActiveUsers(models.Model):
    active_users = models.CharField(max_length=150, unique=True, blank=False, null=False)
    def __str__(self):
        return self.active_users
        