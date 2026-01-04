from rest_framework import serializers
from .models import Tweet

class Tweetserializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model=Tweet
        fields=['id','user', 'text', 'photo', 'created_at', 'update_at']