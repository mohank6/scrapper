from rest_framework import serializers
from app.models import TwitterData, RedditData, YoutubeData
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


class RedditDataSerilizer(serializers.ModelSerializer):

    def validate(self, attrs):
        post_id = attrs.get('post_id')
        reddit_data = RedditData.objects.filter(post_id=post_id).first()
        if reddit_data:
            raise ValidationError('Tweet already exists')
        return super().validate(attrs)

    class Meta:
        model = RedditData
        fields = ['id', 'post_id', 'username', 'text', 'url', 'post_date', 'summary', 'flag']
        extra_kwargs = {'id': {'read_only': True}}


class YoutubeDataSerilizer(serializers.ModelSerializer):

    def validate(self, attrs):
        video_id = attrs.get('video_id')
        video_data = YoutubeData.objects.filter(video_id=video_id).first()
        if video_data:
            raise ValidationError('Video already exists')
        return super().validate(attrs)

    class Meta:
        model = YoutubeData
        fields = ['id', 'video_id', 'text', 'url', 'summary', 'flag']
        extra_kwargs = {'id': {'read_only': True}}


class GeminiDataSerilizer(serializers.Serializer):
    text = serializers.CharField()
    flag = serializers.CharField()
    FLAG_CHOICES = ['news', 'information', 'other']

    def validate(self, attrs):
        flag = attrs.get('flag').lower()
        if flag not in self.FLAG_CHOICES:
            raise ValidationError('Invalid flag')
        return super().validate(attrs)
