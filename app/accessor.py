from app.models import TwitterData


class TwitterDataAccessor():

    @staticmethod
    def filter_tweets(**kwargs):
        return TwitterData.objects.filter(**kwargs)
