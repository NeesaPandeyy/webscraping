from rest_framework import serializers
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_title = serializers.CharField(source='target.title', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'verb',
            'actor_username',
            'target_title',
            'created_at',
            'is_read',
        ]