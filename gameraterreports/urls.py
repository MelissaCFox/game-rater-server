from django.urls import path
from .views import (TopGamesList, BottomGamesList, CategoryGameCountList,
                    MostReviewedGame)

urlpatterns = [
    path('reports/topgames', TopGamesList.as_view()),
    path('reports/bottomgames', BottomGamesList.as_view()),
    path('reports/categorygamecount', CategoryGameCountList.as_view()),
    path('reports/mostreviewedgame', MostReviewedGame.as_view())
]
