import datetime
import os
import json
import random
import pickle
import logging
from time import sleep
from django.conf import settings
from app.gemini import GeminiService

from selectolax.parser import HTMLParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import TimeoutException

from app.serializers import TwitterDataSerilizer, GeminiDataSerilizer
from app.service import TwitterData

log = logging.getLogger('app')


class TwitterScrapper():

    def __init__(self, headless=True) -> None:
        self.home_url = 'https://twitter.com/home'
        self._login_url = 'https://twitter.com/i/flow/_login'
        self.base_url = 'https://twitter.com/'
        self.cookies_folder = 'app/cookies/'
        self.page_source_folder = 'app/page_source/'
        self.cookies_path = 'app/cookies/twitter_cookies.pkl'
        self.is_logged_in = False
        self.WAIT = 2
        self.browser = self._get_browser(headless)

    def _get_browser(self, headless):

        if not os.path.exists(settings.CHROME_DRIVER):
            log.debug('Chrome driver not installed')
            return None

        if not os.path.exists(settings.CHROME_BINARY):
            log.debug('Chrome not installed')
            return None
        try:
            ser = Service(settings.CHROME_DRIVER)
            # ser = Service(ChromeDriverManager().install())

            option = Options()
            option.use_chromium = True
            option.binary_location = str(settings.CHROME_BINARY)
            option.add_experimental_option("excludeSwitches", ["enable-logging"])
            option.add_argument("--disable-extensions")
            option.add_argument("start-maximized")
            option.add_argument("--disable-inforbars")
            option.add_argument("--no-sandbox")
            option.add_argument("dom.disable_beforeunload=true")
            option.add_argument("--log-level=3")
            if headless:
                option.add_argument("headless")
                option.add_argument("--disable-gpu")
            return webdriver.Chrome(service=ser, options=option)
        except Exception as e:
            log.error(f'Error setting up driver: {str(e)}')
            return None

    def _save_page_source(self, filename):
        if not os.path.exists(self.page_source_folder):
            os.makedirs(self.page_source_folder)
        filename = filename + '-' + str(datetime.datetime.now()) + '.html'
        with open(os.path.join(self.page_source_folder, filename), 'w') as fp:
            fp.write(self.browser.page_source)

    def _login(self):
        max_retries = 3
        retries = 0
        while max_retries > retries:
            try:
                self.browser.get(self.lpgin_url)

                username_xpath = '//input[@autocomplete="username"]'
                password_xpath = '//input[@autocomplete="current-password"]'
                # username_xpath = '//input[@data-testid="ocfEnterTextTextInput"]'

                username = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, username_xpath)))
                username.send_keys(settings.TWITTER_USERNAME)
                sleep(random.uniform(self.WAIT, self.WAIT + 1))
                username.send_keys(Keys.RETURN)
                sleep(random.uniform(self.WAIT, self.WAIT + 1))

                password = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, password_xpath)))
                password.send_keys(settings.TWITTER_PASSWORD)
                sleep(random.uniform(self.WAIT, self.WAIT + 1))
                password.send_keys(Keys.RETURN)

                sleep(random.uniform(self.WAIT + 3, self.WAIT + 5))

                self._check_status()
                if self.is_logged_in:
                    self._save_cookies()
                break
            except TimeoutException as e:
                log.debug(f'Timed out: {str(e)}')
            except Exception as e:
                self._save_page_source('_login-exception')
                log.debug(f'_login failed: {str(e)}')
            self.browser.refresh()
            sleep(random.uniform(self.WAIT + 3, self.WAIT + 5))
            retries += 1

    def _save_cookies(self):
        if not os.path.exists(self.cookies_folder):
            os.makedirs(self.cookies_folder)

        # with open(self.cookies_path, 'w') as fp:
        #     json.dump(self.browser.get_cookies(), fp)
        #     log.debug('Cookies saved.')
        pickle.dump(self.browser.get_cookies(), open(self.cookies_path, "wb"))

    def _load_cookies(self):
        if not self._check_for_cookies():
            log.debug('Cookies not found')
            return False
        log.debug('Cookies found')
        try:
            self.browser.get(self.base_url)
            cookies = pickle.load(open(self.cookies_path, "rb"))
            for cookie in cookies:
                self.browser.add_cookie(cookie)
            log.debug('Cookies loaded')
        except Exception as e:
            log.debug(f'Error loading cookies: {str(e)}')
        sleep(random.uniform(self.WAIT, self.WAIT + 4))

    def _check_for_cookies(self):
        return os.path.exists(self.cookies_path)

    def _check_status(self):
        home_xpath = '//a[@data-testid="AppTabBar_Home_Link"]'
        self.browser.get(self.home_url)
        sleep(random.uniform(self.WAIT, self.WAIT + 4))
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, home_xpath)))
            home_page_loaded = True
        except:
            home_page_loaded = False

        if self.browser.current_url == self.home_url and home_page_loaded:
            self.is_logged_in = True
            log.debug(f'_login successfull')
            return
        log.debug(f'_login failed')

    def authenticate(self):
        if not self.browser:
            log.debug('Driver not set up')
            return None

        if not self._check_for_cookies():
            log.debug('Cookies not found')
            self._login()
        else:
            self._load_cookies()

        self._check_status()
        if not self.is_logged_in:
            self._login()
        return None

    def _get_tweet_data(self, card):
        try:
            user = card.find_element(By.XPATH, './/span').text
        except Exception as e:
            log.error(f'Parsing error: {str(e)}')
            return
        try:
            handle = card.find_element(By.XPATH, './/span[contains(text(), "@")]').text
        except Exception as e:
            log.error(f'Parsing error: {str(e)}')
            return
        try:
            postdate = card.find_element(By.XPATH, './/time').get_attribute('datetime')
        except Exception as e:
            log.error(f'Parsing error: {str(e)}')
            return
        try:
            text = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
        except Exception as e:
            log.error(f'Parsing error: {str(e)}')
            return
        try:
            url = card.find_element(By.XPATH, './/a[contains(@href, "/status/")]').get_attribute('href')
        except Exception as e:
            log.error(f'Parsing error: {str(e)}')
            return
        try:
            tweet_id = url.split('/')[-1]
        except Exception as e:
            log.error(f'Parsing error: {str(e)}')
            return
        return {'username': handle, 'user': user, 'post_date': postdate, 'text': text, 'url': url, 'tweet_id': tweet_id}

    def scrape(self, account: str):
        invalid_xpath = '//div[@data-testid="empty_state_header_text"]'
        tweet_card_xpath = '//article[@data-testid="tweet"]'
        scrolling = True
        scrolls = 0
        max_retries = 3
        retries = 0
        tweet_data = []

        if not self.is_logged_in:
            log.debug('Not logged in: call .authenticate()')
            return

        while max_retries > retries:
            self.browser.get(self.base_url + account)
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, invalid_xpath)))
                log.debug('Invalid account')
                return
            except:
                pass
            try:
                while scrolling:
                    sleep(random.uniform(self.WAIT, self.WAIT + 3))
                    tweet_cards = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, tweet_card_xpath)))
                    if not scrolls == 0:
                        tweet_cards = tweet_cards[5:]
                    for card in tweet_cards:
                        data = self._get_tweet_data(card)
                        if not data:
                            continue
                        tweet_data.append(data)
                    # self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    self.browser.execute_script('arguments[0].scrollIntoView();', tweet_cards[-1])
                    if scrolls > 2:
                        scrolling = False
                    scrolls += 1
                breakpoint()
            except Exception as e:
                log.debug(f'Could not find tweets: {str(e)}')
                retries += 1
                continue

            for data in tweet_data:
                serializer = TwitterDataSerilizer(data=data)
                if not serializer.is_valid():
                    continue
                serializer.save()
                log.debug('Tweet saved')
            break


class Summarizer():

    @classmethod
    def _get_summarized_data(cls, tweet_data):
        gemini = GeminiService()
        data = gemini.generate_completion(tweet_data.text)
        if not data:
            log.debug('No data')
            return
        gemini_serializer = GeminiDataSerilizer(data=data)
        if not gemini_serializer.is_valid():
            log.debug(gemini_serializer.errors)
            return
        tweet_data.summary = gemini_serializer.validated_data.get('text')
        tweet_data.flag = gemini_serializer.validated_data.get('flag')
        tweet_data.is_summarized = True
        tweet_data.save()
        log.debug('Tweet updated')

    @classmethod
    def summarize(cls):
        tweets = TwitterData.get_not_summarized_tweets()
        for tweet in tweets:
            print(tweet)
            cls._get_summarized_data(tweet)
        log.debug('Tweets summarized')
