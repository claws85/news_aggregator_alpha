
from django.shortcuts import render
from django.views import View

from config.settings.common import GROUP_TITLES, KEYWORDS
from datetime import datetime, timedelta
from news_aggregator_alpha.models import Article
from news_aggregator_alpha.utils import NewsGatherer


class HomeView(View):
    def get(self, request):

        dict_list = []
        search_set = set()

        for k in KEYWORDS:

            gatherer = NewsGatherer(
                k, 2
            )
            gatherer.run_process()

            search_set.add(k.split(' ')[0])
        
        for s in search_set:
            dict_list.append(
                {
                    GROUP_TITLES.get(s) :
                    NewsGatherer.return_todays_articles_by_first_keyword(s)
                }
            )

        context = {
            'd_list' : dict_list
            }

        return render(request, 'index.html', context)

class ArchiveView(View):
    def get(self, request):

        dict_list = []
        search_set = set()

        for k in KEYWORDS:
            search_set.add(k.split(' ')[0])

        all_articles = Article.objects.all()

        for day in range(1,8):
            dt = datetime.now() - timedelta(days=day)
            articles = all_articles.filter(
                date__lte=dt
                )
            
            date_dict = {dt.strftime("%d %B, %Y") : {}}
            
            for s in search_set:
                sub_dict = {
                    GROUP_TITLES.get(s) :
                    articles.filter(keywords__startswith=s)
                }

                date_dict[dt.strftime("%d %B, %Y")].update(sub_dict)
            
            dict_list.append(
                date_dict
            )

        context = {'d_list' : dict_list}

        return render(request, 'archive.html', context)