from django.contrib import admin
from app.models import TwitterData, RedditData, YoutubeData
from app.summarizer import Summarizer


@admin.action(description="Summarize Tweets")
def summarize_tweets(modeladmin, request, queryset):
    new_query_set = queryset.filter(is_summarized=False)
    Summarizer.summarize_tweets(new_query_set)


@admin.action(description="Summarize Reddit Posts")
def summarize_reddit(modeladmin, request, queryset):
    new_query_set = queryset.filter(is_summarized=False)
    Summarizer.summarize_reddit(new_query_set)


@admin.action(description="Summarize Youtube Transcripts")
def summarize_transcript(modeladmin, request, queryset):
    new_query_set = queryset.filter(is_summarized=False)
    Summarizer.summarize_transcript(new_query_set)


class BaseAdminModel(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return []
        fields = ([f.name for f in self.model._meta.fields])
        return fields


@admin.register(TwitterData)
class TwitterDataAdmin(BaseAdminModel):
    list_display = ('tweet_id', 'url', 'is_summarized', 'flag')
    actions = [summarize_tweets]


@admin.register(RedditData)
class RedditDataAdmin(BaseAdminModel):
    list_display = ('post_id', 'url', 'is_summarized', 'flag')
    actions = [summarize_reddit]


@admin.register(YoutubeData)
class YoutubeDataAdmin(BaseAdminModel):
    list_display = ('video_id', 'url', 'is_summarized', 'flag')
    actions = [summarize_transcript]
