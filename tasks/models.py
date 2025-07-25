from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


# Create your models here.
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', '-created']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        # This will ensure that the tasks are ordered by completion status and creation date