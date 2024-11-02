from django.shortcuts import render

from .models import Player

# Create your views here.
def player_list(request):
    # Query the database for all players
    players = Player.objects.all()
    
    # Pass the players to the template
    return render(request, 'player_list.html', {'players': players})