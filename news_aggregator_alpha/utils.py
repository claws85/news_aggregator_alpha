
from datetime import date, datetime, timedelta
import logging
import requests

from config.settings.common import API_KEY
from django.db import transaction
from news_aggregator_alpha.models import Article

logger = logging.getLogger(__name__)

class NewsGatherer(object):
    def __init__(self, countries_param, search_terms_param, pages):
        self.base_url = 'https://newsdata.io/api/1/news'
        self.api_key = API_KEY
        self.countries = countries_param
        self.search_terms = search_terms_param
        self.pages = pages

    def update_needed(self):
        try:
            latest = Article.objects.latest()
            if latest.date == date.today():
                return False
            return True

        except Article.DoesNotExist:
            return True
    
    def create_url(self, page):
        # needed as requests payload causing issues with spaces
        url = self.base_url + '?' +  'apikey=' + self.api_key
        url += '&country=' + self.countries
        url += '&language=en'
        url += '&q=' + self.search_terms
        return url + '&page=' + str(page)

    def get_articles_json(self, page):

        url = self.create_url(page)        
        r = requests.get(url)

        if r.status_code == 200:
            return r.json()

        raise ValueError(
            "A {} status code was recieved when attempting to \
            retrieve data from the API at {}.".format(
                r.status_code,
                datetime.now()
                )
        )
        
    def create_articles(self, json):
        titles_set = set()

        for article in json.get('results'):
            if not article.get('title'):
                logger.warn("Article had no title, so was ommitted.")
                continue

            if article.get('title') in titles_set:
                continue
            titles_set.add(article.get('title'))
            
            self.create_article(article)

    
    @transaction.atomic
    def create_article(self, article):

        try:
            Article.objects.create(
                title=article.get('title'),
                url = article.get('link'),
                source = article.get('source_id'),
            )
        except Exception as e:
            logger.error(
                "The following error occurred when attempting to \
                create an article: {}".format(e)
            )

    @staticmethod
    def get_old_articles():
        old_articles = Article.objects.filter(
                date__lte=datetime.now() - timedelta(days=7)
                )
        if old_articles:
            return old_articles
    
    @staticmethod
    def return_todays_articles():
        return Article.objects.filter(
            date__gte=date.today()
        )

    def run_process(self):
        try:
            if self.update_needed():
                for p in range(self.pages):
                    json = self.get_articles_json(p)
                    self.create_articles(json)
            
            old_articles = self.get_old_articles()
            if old_articles:
                old_articles.delete()


        except Exception as e:
            logging.error(
                "The following error occurred when attemtpting to \
                retrieve articles from the API and save them: \
                {}".format(e)
                )
