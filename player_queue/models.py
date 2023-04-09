from django.db import models

# Create your models here.

class url(models.Model):
    yt_url = models.CharField(max_length=90, null=False, unique=False, blank=False)
    def __str__(self):
        return self.yt_url