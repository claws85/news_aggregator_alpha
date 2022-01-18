
from datetime import date, datetime, timedelta
import logging
import pyshorteners
import requests
import time

from config.settings.common import API_KEY, SINGLE_ISSUE_TOPICS
from django.db import transaction
from news_aggregator_alpha.models import Article

logger = logging.getLogger(__name__)

class NewsGatherer(object):
    def __init__(self, search_terms_param, pages):
        self.base_url = 'https://gnews.io/api/v4/search'
        self.api_key = API_KEY
        self.search_terms = search_terms_param
        self.pages = pages
        self.titles_list = []
        self.links_list = []

    def update_needed(self):
        try:
            q = Article.objects.filter(keywords__startswith=self.search_terms)
            if q.latest().date == date.today():
                return False
            return True

        except Article.DoesNotExist:
            return True
    
    def create_url(self, page):
        url = self.base_url + '?' +  'token=' + self.api_key
        url += '&lang=en'
        url += '&q=' + self.search_terms
        return url + '&page=' + str(page)

    def get_articles_json(self, page):
        time.sleep(1)
        url = self.create_url(page)        
        print(url)
        r = requests.get(url)
        print(r.status_code)
        if r.status_code == 200:
            return r.json()

        raise ValueError(
            """A {} status code was recieved when attempting to 
            retrieve data from the API at {}.""".format(
                r.status_code,
                datetime.now()
                )
        )
        
    def create_articles(self, json):

        for article in json.get('articles'):
            print(article['title'])
            if not article.get('title'):
                logger.warn("Article had no title, so was ommitted.")
                continue

            if (
                    article.get('title') in self.titles_list or
                    article.get('url') in self.links_list
            ):
                continue

            self.titles_list.append(article.get('title'))
            self.links_list.append(article.get('url'))
            
            article = self.manage_lengths(article)

            self.create_article(article)

    @staticmethod
    def manage_lengths(article):
        if len(article.get('title')) > 200: 
            article['title'] = article.get('title')[:200]
        if len(article.get('url')) > 200:
            s = pyshorteners.Shortener()
            article['url'] = s.tinyurl.short(article.get('url'))
        return article
    
    @transaction.atomic
    def create_article(self, article):       
        print(article['title'])
        try:
            Article.objects.create(
                title=article.get('title'),
                url = article.get('url'),
                source = article.get('source').get('name'),
                keywords = self.search_terms
            )
        except Exception as e:
            logger.error(
                """The following error occurred when attempting to 
                create an article: {}""".format(e)
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

    @staticmethod
    def return_articles_by_keywords(keywords):
        return Article.objects.filter(
            keywords=keywords
        )
    
    @staticmethod
    def return_articles_by_first_keyword(first_keyword):
        return Article.objects.filter(
            keywords__startswith=first_keyword
        )
    
    def check_sufficient_articles(self):
        count = 0
        while count < 5:
            
            if (
                self.return_articles_by_keywords(self.search_terms).count()
                < 10
            ):
                break
            else:
                json = self.get_articles_json(self.pages)
                self.create_articles(json)
                self.pages += 1
                count += 1

    def run_process(self):
        try:
            if self.update_needed():
                for p in range(self.pages):
                    json = self.get_articles_json(p)
                    self.create_articles(json)
                
                if self.search_terms in SINGLE_ISSUE_TOPICS:
                    self.check_sufficient_articles()
            
            old_articles = self.get_old_articles()
            if old_articles:
                old_articles.delete()


        except Exception as e:
            logging.error(
                """The following error occurred when attemtpting to 
                retrieve articles from the API and save them: 
                {}""".format(e)
                )
