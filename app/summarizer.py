from app.gemini import GeminiService
from app.serializers import GeminiDataSerilizer
import logging

from app.service import TwitterData, RedditData, YoutubeData

log = logging.getLogger('app')


class Summarizer():

    @classmethod
    def _get_summarized_data(cls, data):
        gemini = GeminiService()
        response = gemini.generate_completion(data.text)
        if not response:
            log.debug('No data from gemini')
            return
        gemini_serializer = GeminiDataSerilizer(data=response)
        if not gemini_serializer.is_valid():
            log.debug(gemini_serializer.errors)
            return
        data.summary = gemini_serializer.validated_data.get('text')
        data.flag = gemini_serializer.validated_data.get('flag')
        data.is_summarized = True
        data.save()

    @classmethod
    def summarize_tweets(cls):
        tweets = TwitterData.get_not_summarized_tweets()
        for tweet in tweets:
            cls._get_summarized_data(tweet)
        log.debug('Tweets summarized')

    @classmethod
    def summarize_reddit(cls):
        posts = RedditData.get_not_summarized_posts()
        for post in posts:
            cls._get_summarized_data(post)
        log.debug('Posts summarized')

    @classmethod
    def summarize_transcript(cls):
        transcripts = YoutubeData.get_not_summarized_transcripts()
        for transcript in transcripts:
            cls._get_summarized_data(transcript)
        log.debug('Transcirpts summarized')
