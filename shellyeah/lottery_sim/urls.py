from django.urls import path
from . import views

urlpatterns = [
    path('get_league_id/', views.league_id, name='get_league_id'),
    path('<int:league_id>/', views.get_odds, name='get_odds'),
    path('<int:league_id>/results/', views.lottery_results, name='lottery_results'),
]
