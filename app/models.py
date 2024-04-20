from django.db import models
from app.utils import get_char_uuid


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, max_length=100, db_index=True, editable=False, default=get_char_uuid)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TwitterData(BaseModel):
    NEWS = 'news'
    INFORMATION = 'information'
    OTHER = 'other'
    FLAG_CHOICES = (
        (NEWS, NEWS),
        (INFORMATION, INFORMATION),
        (OTHER, OTHER),
    )
    tweet_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    text = models.TextField()
    url = models.URLField(max_length=255)
    post_date = models.DateTimeField()
    is_summarized = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)
    flag = models.CharField(max_length=255, choices=FLAG_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.username} - {self.tweet_id}'


class RedditData(BaseModel):
    NEWS = 'news'
    INFORMATION = 'information'
    OTHER = 'other'
    FLAG_CHOICES = (
        (NEWS, NEWS),
        (INFORMATION, INFORMATION),
        (OTHER, OTHER),
    )
    post_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    text = models.TextField()
    url = models.URLField(max_length=255)
    post_date = models.DateTimeField()
    is_summarized = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)
    flag = models.CharField(max_length=255, choices=FLAG_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.username} - {self.post_id}'


class YoutubeData(BaseModel):
    NEWS = 'news'
    INFORMATION = 'information'
    OTHER = 'other'
    FLAG_CHOICES = (
        (NEWS, NEWS),
        (INFORMATION, INFORMATION),
        (OTHER, OTHER),
    )
    video_id = models.CharField(max_length=255)
    text = models.TextField()
    url = models.URLField(max_length=255)
    post_date = models.DateTimeField()
    is_summarized = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)
    flag = models.CharField(max_length=255, choices=FLAG_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.video_id}'
