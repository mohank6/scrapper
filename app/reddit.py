from datetime import datetime, timezone
from urllib.parse import urljoin
import praw
from django.conf import settings
from prawcore.exceptions import Redirect, ResponseException
import logging

from app.serializers import RedditDataSerilizer

log = logging.getLogger('app')


class RedditScrapper():
    def __init__(self):
        self._reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USERAGENT,
            # username=settings.REDDIT_USERNAME,
            # password=settings.REDDIT_PASSWORD,
        )

    def _clean_post(self, post):
        delimiter = '\n'
        post_id = post.id
        username = post.author.name
        text = delimiter.join([post.title, post.selftext]).strip()
        url = urljoin('https://www.reddit.com/', post.permalink)
        post_date = datetime.fromtimestamp(post.created_utc, timezone.utc)
        return {
            'post_id': post_id,
            'username': username,
            'text': text,
            'url': url,
            'post_date': post_date,
        }

    def scrape(self, subreddit, limit=50):
        subreddit = self._reddit.subreddit(subreddit)
        try:
            full_name = subreddit.fullname
        except Redirect as e:
            log.debug(f'Invalid subreddit: {repr(e)}')
        except ResponseException as e:
            log.debug(f'Invalid authentication: {repr(e)}')
        except Exception as e:
            log.debug(f'Error occured: {repr(e)}')
        log.debug('Fetching posts...')
        posts = [post for post in subreddit.new(limit=limit)]
        for post in posts:
            data = self._clean_post(post)
            serializer = RedditDataSerilizer(data=data)
            if not serializer.is_valid():
                continue
            serializer.save()
            log.debug('Post saved')
