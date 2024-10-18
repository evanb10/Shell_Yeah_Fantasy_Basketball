from django.urls import path
from . import views

urlpatterns = [
    path('', views.players, name='players'),
    path('contact/',views.contact, name='contact'),
#     path('sim_lottery/get_league_id/', views.league_id, name='get_league_id'),
#     path('sim_lottery/<int:league_id>/', views.get_odds, name='get_odds'),
#     path('sim_lottery/<int:league_id>/results', views.lottery_results, name='lottery_results'),
]
