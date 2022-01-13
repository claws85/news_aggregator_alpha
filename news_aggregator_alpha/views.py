
from django.shortcuts import render
from django.views import View

from news_aggregator_alpha.utils import NewsGatherer


class IndexView(View):
    def get(self, request):

        gatherer = NewsGatherer(
            'gb,us,au', 'russia%20AND%20ukraine', 2
            )
        gatherer.run_process()

        # return articles from created today
        context = {
            'articles' : gatherer.return_todays_articles()
            }

        return render(request, 'index.html', context)
