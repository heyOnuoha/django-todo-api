from django.db import models

from django.db import models
from django.utils import timezone

class TodoItem(models.Model):

    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=True, default='')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)
    

    def __str__(self):

        return self.title
