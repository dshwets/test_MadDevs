from django.contrib.postgres.fields import JSONField
from django.db import models


class Links(models.Model):
    link = models.URLField(max_length=200, verbose_name="Repository link")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Added')

    def __str__(self):
        return self.link


class CommitsHistory(models.Model):
    link = models.ForeignKey(Links, on_delete=models.CASCADE, verbose_name='Link',
                             related_name='links')
    commit_id = models.CharField(max_length=200, verbose_name='Commit hash')
    commit_json = models.TextField(verbose_name='Commit text')

    def __str__(self):
        return self.commit_id
