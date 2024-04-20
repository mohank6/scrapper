from app.models import TwitterData, RedditData


class TwitterDataAccessor():

    @staticmethod
    def filter_tweets(**kwargs):
        return TwitterData.objects.filter(**kwargs)


class RedditDataAccessor():

    @staticmethod
    def filter_posts(**kwargs):
        return RedditData.objects.filter(**kwargs)
