from app.models import TwitterData, RedditData, YoutubeData


class TwitterDataAccessor():

    @staticmethod
    def filter_tweets(**kwargs):
        return TwitterData.objects.filter(**kwargs)


class RedditDataAccessor():

    @staticmethod
    def filter_posts(**kwargs):
        return RedditData.objects.filter(**kwargs)


class YoutubeDataAccessor():

    @staticmethod
    def filter_transcripts(**kwargs):
        return YoutubeData.objects.filter(**kwargs)
