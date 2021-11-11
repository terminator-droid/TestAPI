from rest_framework import serializers
from .models import Tasks


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'header', 'text', 'date', 'done')
