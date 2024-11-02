from django.shortcuts import render

from .models import Player

# Create your views here.
def player_list(request):
    # Query the database for all players
    players = Player.objects.all()
    
    # Pass the players to the template
    return render(request, 'player_list.html', {'players': players})

# def players(request):
#     ''' Players Page '''
#     # filter form to be displayed. 
#     # form = players_form.PlayerForm(request.POST or None)

#     # Context that will be sent to the associated template
#     context = {}

#     # Begin request logic
#     if request.method == "POST":

#         # Verify that the form is valid using built-in Django
#         # if form.is_valid():
#         if True:
#             # Determine if filters are present in the request. True or False
#             on_roster_exists = "on_roster" in request.POST
#             managers_exist = "managers" in request.POST

#             # If user chose on roster and a manager AND the manager chosen was not the None option
#             if (on_roster_exists and managers_exist) and not('None' in request.POST['managers']):
#                 pass
#                 # # From Rosters table, pull player ids with the manager_id associated with the manager selected from the form. 
#                 # manager_query = Roster.objects.filter(manager_id=request.POST['managers']).values_list('player_id',flat=True)
#                 # # Use the select players from the previous command to get the player info from player table. 
#                 # players_from_second_table = Player.objects.filter(player_id__in=manager_query).values()
#                 # # Get all players from table, but exclude all players not on actual NBA rosters
#                 # players = Player.objects.exclude(team=None)
#                 # # Get the intersection of the two queries.  
#                 # intersection = players_from_second_table.intersection(players)
#                 # # Get Manager team name using manager id number from form
#                 # manager = Manager.objects.filter(manager_id=request.POST['managers']).only('team_name')
#                 # # Set the context equal to the intersection
#                 # context['players'] = intersection
#                 # context['caption'] = "List of NBA Players on " + str(manager[0]) + " roster"


#             # If the user chose on roster filter ONLY
#             elif on_roster_exists:
#                 # Get all players from table, but exclude all players not on actual NBA rosters
#                 players = Player.objects.exclude(team=None)
#                 # Set the context equal to the intersection
#                 context['players'] = players
#                 context['caption'] = "List of NBA Players on Rosters"
                
#             # If the user chose a manager filter ONLY
#             elif managers_exist:
#                 # If the manager chosen was not the None option
#                 if not('None' in request.POST['managers']):
#                     pass
#                     # # From Rosters table, pull player ids with the manager_id associated with the manager selected from the form. 
#                     # manager_query = Roster.objects.filter(manager_id=request.POST['managers']).values_list('player_id',flat=True)
#                     # # Use the select players from the previous command to get the player info from player table. 
#                     # players_from_second_table = Player.objects.filter(player_id__in=manager_query).values()
#                     # # Get Manager team name using manager id number from form
#                     # manager = Manager.objects.filter(manager_id=request.POST['managers']).only('team_name')
#                     # context['caption'] = "List of NBA Players on " + str(manager[0]) + " roster"
#                     # # Set the context equal to the players
#                     # context['players'] = players_from_second_table
#                 else:
#                     # If the -- None -- option was chosen from the players form.
#                     players = Player.objects.all().values()
#                     # Set the context equal to the players
#                     context['players'] = players
#             else:
#                 # If no option is selected
#                 players = Player.objects.all().values()
#                 # Set the context equal to the players
#                 context['players'] = players
#         else:
#             # Print the error fromt he form
#             print(form.errors)
#     else:
#         # Initial GET request so just pull all players from database
#         players = Player.objects.all().values()
#         # Set the context equal to the players
#         context['players'] = players
#     # Add the form to the context
#     # context['form'] = form
       
#     return render(request,'players.html',context)