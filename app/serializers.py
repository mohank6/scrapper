from rest_framework import serializers
from app.models import TwitterData
from django.core.exceptions import ValidationError


class TwitterDataSerilizer(serializers.ModelSerializer):

    def validate(self, attrs):
        tweet_id = attrs.get('tweet_id')
        tweet_data = TwitterData.objects.filter(tweet_id=tweet_id).first()
        if tweet_data:
            raise ValidationError('Tweet already exists')
        return super().validate(attrs)

    class Meta:
        model = TwitterData
        fields = ['id', 'tweet_id', 'username', 'text', 'url', 'post_date', 'summary', 'flag']
        extra_kwargs = {'id': {'read_only': True}}


class GeminiDataSerilizer(serializers.Serializer):
    text = serializers.CharField()
    flag = serializers.CharField()
    FLAG_CHOICES = ['news', 'information', 'other']

    def validate(self, attrs):
        flag = attrs.get('flag').lower()
        print(flag)
        if flag not in self.FLAG_CHOICES:
            raise ValidationError('Invalid flag')
        return super().validate(attrs)
