from django.urls import path
from . import views

urlpatterns = [
    path('get_user_name/', views.get_user_name, name='get_user_name'),
    path('<int:league_id>/', views.get_odds, name='get_odds'),
    path('<int:league_id>/results/', views.lottery_results, name='lottery_results'),
    path('<slug:user_name>/leagues/', views.user_leagues, name='user_leagues'),
]
