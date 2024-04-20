from app.accessor import TwitterDataAccessor, RedditDataAccessor, YoutubeDataAccessor


class TwitterData:

    @staticmethod
    def get_not_summarized_tweets():
        return TwitterDataAccessor.filter_tweets(is_summarized=False)


class RedditData:

    @staticmethod
    def get_not_summarized_posts():
        return RedditDataAccessor.filter_posts(is_summarized=False)


class YoutubeData:

    @staticmethod
    def get_not_summarized_transcripts():
        return YoutubeDataAccessor.filter_transcripts(is_summarized=False)
