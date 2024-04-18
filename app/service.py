from app.accessor import TwitterDataAccessor


class TwitterData:

    @staticmethod
    def get_not_summarized_tweets():
        return TwitterDataAccessor.filter_tweets(is_summarized=False)
