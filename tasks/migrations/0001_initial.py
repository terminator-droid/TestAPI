# Generated by Django 3.2.9 on 2021-11-09 10:31

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TasksModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('header', models.CharField(max_length=30)),
                ('text', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('done', models.CharField(default='Нет', max_length=3)),
            ],
        ),
    ]
