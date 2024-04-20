import re
from youtube_transcript_api import YouTubeTranscriptApi

import logging

from app.serializers import YoutubeDataSerilizer

log = logging.getLogger('app')


class YoutubeTranscriptScrapper():

    def __init__(self):
        self.base_urls = ['https://www.youtube.com/watch?v=', ]

    def _get_video_id(self, video_url):
        pattern = (
            r"(?:https?://)?(?:www\.)?"
            r"(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)"
            r"([^\"&?/ ]{11})"
        )
        match = re.search(pattern, video_url)
        if match:
            return match.group(1)
        else:
            return None

    def _clean_data(self, text, video_url, video_id):
        return {
            'text': text,
            'url': video_url,
            'video_id': video_id,
        }

    def _clean_transcript(self, transcript):
        text = ''
        for item in transcript:
            sentence = item['text']
            text += f'{sentence}\n'
        return text.strip()

    def scrape(self, video_url):
        video_id = self._get_video_id(video_url)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            log.error(f'Error fetching transcript: {str(e)}')
            return
        clened_transcript = self._clean_transcript(transcript)
        data = self._clean_data(clened_transcript, video_url, video_id)
        serializer = YoutubeDataSerilizer(data=data)
        if not serializer.is_valid():
            log.error(f'Error saving transcript: {serializer.errors}')
            return
        serializer.save()
        log.info('Transcript saved')
