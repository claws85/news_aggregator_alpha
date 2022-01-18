
from django.shortcuts import render
from django.views import View

from news_aggregator_alpha.utils import NewsGatherer
from config.settings.common import GROUP_TITLES, KEYWORDS


class IndexView(View):
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
