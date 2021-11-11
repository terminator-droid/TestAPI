from django.db import models
import uuid
from datetime import date


class TasksModel(models.Model):
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    header = models.CharField(max_length=30)
    text = models.TextField()
    date = models.DateField(default=date.today, )
    done = models.CharField(max_length=3, default='Нет')

    def __str__(self):
        return self.header
