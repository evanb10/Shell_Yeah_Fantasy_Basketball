import re
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
# from .models import Player#, Roster, Manager, League, LeagueMembership
from .forms import players_form, league_id_form, odds_form, contact_form
from .scripts.lottery import League as script_league, Team as script_team
from .scripts.sleeper import League as sleeper_league

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Subquery




# Create your views here.

# def player_list(request):
#     # Query the database for all players
#     players = Player.objects.all()
    
#     # Pass the players to the template
#     return render(request, 'player_list.html', {'players': players})




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

# def league_id(request):
#     context = {}
#     # if this is a POST request we need to process the form data
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         id_form = league_id_form.LeagueForm(request.POST)

#         # check whether it's valid:
#         if id_form.is_valid():
#             # Get league id
#             league_id = request.POST['league_id']
            
#             sleeper = sleeper_league(league_id)
#             # Update league 
#             sleeper.get_league_api()
#             #Update managers
#             sleeper.get_managers()
#             # sleeper.clear_managers_table()
#             sleeper.save_managers_to_database()

#             #Update rosters
#             sleeper.get_rosters()
#             return redirect(reverse('get_odds', kwargs={'league_id': league_id}))

#             # Pull all information about a league given the provided league ID

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = league_id_form.LeagueForm()
#         context['form'] = form
#     return render(request, 'league_id_form.html',context)

# def get_odds(request,league_id):
#     context = {}
#     def odds(num):
#         odds_dict = {
#             12:[30,25,20,15,10,0,0,0,0,0,0,0],
#             10:[40,30,20,10,0,0,0,0,0,0],
#             8:[45,35,20,0,0,0,0,0],
#             }
#         return odds_dict[num]
    
#     # Define a function to calculate wins from the record string
#     def get_wins(record):
#         if not record:
#             return 0
#         return record.count('W')
    
#     def extract_percentage_values(data):
#         percentage_values = []
#         for key, value in data.items():
#             if key.startswith('percentage_'):
#                 clean_key = key.replace('percentage_', '')
#                 percentage_values.append((clean_key, int(value)))        
#         return percentage_values

#     league_query = League.objects.filter(league_id=league_id).values().first()
#     if league_query:
#         # Prepare context data
#         memebership_query = LeagueMembership.objects.filter(league_id=league_id).values_list('manager_id',flat=True)
#         print(memebership_query)
#         teams = Manager.objects.filter(manager_id__in=Subquery(memebership_query))
#         print(teams)

#         # teams = Manager.objects.filter(league_id=league_id)
#         league_ = script_league()
#         for manager in teams:
#             manager_name = manager.display_name
#             # odds_ = teams['percentage_' + manager_name]
#             wins = manager.wins
#             losses = manager.losses
#             points_for = manager.points_for
#             points_against = manager.points_against


#             new_team = script_team(manager_name, 0, wins, losses, points_for, points_against)
#             league_.addTeam(new_team)
    
#         league_.sort_teams()
#         odds_values = odds(league_query['num_of_teams'])
#         for idx,team in enumerate(league_.teams,start=1):
#             team.odds = odds_values[-idx]
#         # sorted_list = sorted(teams, key=lambda x: (get_wins(x[1]), x[0]))
#         # zipped_data = zip([team[0] for team in sorted_list], odds_values)
#         # teams_list = list(zipped_data)
#         context['teams'] = league_.teams
#     else:
#         return HttpResponseBadRequest("League not found.")

#     if request.method == "POST":
#         # teams = extract_percentage_values(request.POST)
#         form_odds = odds_form.PercentageAllocationForm(request.POST or None, teams=league_.teams)

#         if form_odds.is_valid():
#             cleaned_data = form_odds.cleaned_data
#             # Process cleaned data
#             return redirect(reverse('lottery_results', kwargs={'league_id': league_id})+ f'?cleaned_data={cleaned_data}')
#         else:
#             context['form'] = form_odds  # Pass the form with errors to the template
#             return render(request, 'lottery_sim.html', context)

#     else:

#             form_odds = odds_form.PercentageAllocationForm(teams=league_.teams[::-1])
#             context['form'] = form_odds
#             return render(request, 'lottery_sim.html', context)



# def lottery_results(request, league_id):
#     from django.http import HttpResponse
#     from .scripts.lottery import League, Team
#     import json, time
#     teams = request.GET.get('cleaned_data')
#     print(teams)

#     if teams:
#         try:
#             # Replace single quotes with double quotes
#             teams_str = teams.replace("'", '"')

#             # Replace Decimal('value') with float value
#             teams_str = re.sub(r'Decimal\("([\d.]+)"\)', r'\1', teams_str)

#             # Convert the JSON string to a dictionary
#             teams_dict = json.loads(teams_str)

#             league = League()
#             for manager, odds in teams_dict.items():
#                 manager_name = manager[len('percentage_'):]
#                 odds = float(odds)  # Ensure odds is a float
#                 manager_model = Manager.objects.get(display_name=manager_name)
#                 wins = manager_model.wins
#                 losses = manager_model.losses
#                 points_for = manager_model.points_for
#                 points_against = manager_model.points_against

#                 new_team = Team(manager_name, odds, wins, losses, points_for, points_against)
#                 league.addTeam(new_team)

#             league.sort_teams()
#             league.setRanks()
#             league.splitOdds()
#             league.oddsCheck()
#             league.splitCombinations()
#             league.teams.sort(key=lambda x: x.rank, reverse=True)
#             league.findWinningTeam()

#             context = {'results': league.lottery_results}
#             return render(request, 'lottery_sim_results.html', context)

#         except (json.JSONDecodeError, Manager.DoesNotExist, ValueError) as e:
#             # Handle possible errors
#             print(f"Error processing request: {e}")
#             return HttpResponseBadRequest("Invalid data format or manager not found.")
#     else:
#         # Handle the case where cleaned_data is not provided
#         return HttpResponseBadRequest("No data provided.")

def contact(request):
    print(request.method)
    if request.method == 'POST':
        form = contact_form.ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            html = render_to_string('contactform.html', {
                'name': name,
                'subject': subject,
                'email': email,
                'message': message,
            })
            send_mail('The contact form subject','this is the message','eablake153@gmail.com',['eablake153@gmail.com'], html_message=html)
            content = {
                "result": "Message was successfully submitted."

            }
    else:
        form = contact_form.ContactForm()
        content = {
            "form": form,
        }

    return render(request,'contact.html',content)
    
