from django.db import models

class Links(models.Model):
    link = models.URLField(max_length=200, verbose_name="Repository link")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Added')