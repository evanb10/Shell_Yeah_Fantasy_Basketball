import re
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from lottery_sim.models import League

# from .models import Player#, Roster, Manager, League, LeagueMembership
from .forms import user_name_form, odds_form
from .scripts.lottery import League as script_league, Team as script_team
from .scripts.sleeper import League as sleeper_league


from django.db.models import Subquery

import shellyeah.scripts.sleeper as sleeper




# Create your views here.

def get_user_name(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        id_form = user_name_form.UserNameForm(request.POST)

        # check whether it's valid:
        if id_form.is_valid():
            # Get league id
            league_id = request.POST['league_id']
            
            # Update league 
            # sleeper.get_league_api(league_id)
            #Update managers
            sleeper.update_managers(league_id)
            # sleeper.clear_managers_table()
            # sleeper.save_managers_to_database()

            #Update rosters
            # sleeper.get_rosters()
            return redirect(reverse('get_odds', kwargs={'league_id': league_id}))

            # Pull all information about a league given the provided league ID

    # if a GET (or any other method) we'll create a blank form
    else:
        form = user_name_form.UserNameForm()
        context['form'] = form
    return render(request, 'league_id_form.html',context)

def get_odds(request,league_id):
    context = {}
    def odds(num):
        odds_dict = {
            12:[30,25,20,15,10,0,0,0,0,0,0,0],
            10:[40,30,20,10,0,0,0,0,0,0],
            8:[45,35,20,0,0,0,0,0],
            }
        return odds_dict[num]
    
    def extract_percentage_values(data):
        percentage_values = []
        for key, value in data.items():
            if key.startswith('percentage_'):
                clean_key = key.replace('percentage_', '')
                percentage_values.append((clean_key, int(value)))        
        return percentage_values

    league_query = League.objects.filter(league_id=league_id).values().first()
    
    if league_query:
        prev_league = league_query['previous_league_id']
        prev_records = sleeper.get_prev_league_api(prev_league)

        # teams = Manager.objects.filter(league_id=league_id)
        league_ = script_league()
        for manager in prev_records.items():
            manager_name = manager[1]['user_name']
            # odds_ = teams['percentage_' + manager_name]
            wins = manager[1]['wins']
            losses = manager[1]['losses']
            points_for = manager[1]['pf']
            points_against = manager[1]['pa']


            new_team = script_team(manager_name, 0, 0, wins, losses, points_for, points_against)
            league_.addTeam(new_team)
    
        league_.sort_teams()
        odds_values = odds(league_query['num_of_teams'])
        for idx,team in enumerate(league_.teams,start=1):
            team.odds = odds_values[-idx]
        context['teams'] = league_.teams
    else:
        return HttpResponseBadRequest("League not found.")

    if request.method == "POST":
        # print(league_query)
        # teams = extract_percentage_values(request.POST)
        form_odds = odds_form.PercentageAllocationForm(request.POST or None, teams=league_.teams)

        if form_odds.is_valid():
            cleaned_data = form_odds.cleaned_data
            # Step 1: Update odds for each team based on the cleaned_data
            for team in league_.teams:
                team_name = team.name
                # Assuming `cleaned_data` contains team names as keys and odds as values
                if f'percentage_{team_name}' in cleaned_data:
                    team.odds = cleaned_data[f'percentage_{team_name}']
            
            # Step 2: Store the updated teams in the session for the next view
            request.session['updated_teams'] = [
                {
                    'name': team.name,
                    'rank': team.rank,
                    'wins': team.wins,
                    'losses': team.losses,
                    'odds': float(team.odds),
                    'points_for': float(team.points_for),
                    'points_against': float(team.points_against),
                }
                for team in league_.teams
            ]
            
            # Redirect to the lottery results view
            return redirect(reverse('lottery_results', kwargs={'league_id': league_id}))
        else:
            context['form'] = form_odds  # Pass the form with errors to the template
            return render(request, 'lottery_sim.html', context)

    else:

            form_odds = odds_form.PercentageAllocationForm(teams=league_.teams[::-1])
            context['form'] = form_odds
            return render(request, 'lottery_sim.html', context)



def lottery_results(request, league_id):
    from django.http import HttpResponse
    from .scripts.lottery import League, Team
    import json, time
    # teams = request.GET.get('cleaned_data')
    # print(teams)
    updated_teams = request.session.get('updated_teams')
    # print(updated_teams)

    teams = updated_teams

    if teams:
        try:
            # Replace single quotes with double quotes
            # teams_str = teams.replace("'", '"')

            # Replace Decimal('value') with float value
            # teams_str = re.sub(r'Decimal\("([\d.]+)"\)', r'\1', teams_str)

            # Convert the JSON string to a dictionary
            # teams_dict = json.loads(teams_str)

            league = League()
            print(teams)
            for manager in teams:
                manager_name = manager['name']
                odds = manager['odds']  # Ensure odds is a float
                # manager_model = Manager.objects.get(display_name=manager_name)
                wins = manager['wins']
                losses = manager['losses']
                points_for = manager['points_for']
                points_against = manager['points_against']
                rank = manager['rank']

                new_team = Team(manager_name, rank, odds, wins, losses, points_for, points_against)
                league.addTeam(new_team)

            league.sort_teams()
            league.setRanks()
            league.splitOdds()
            league.oddsCheck()
            league.splitCombinations()
            league.teams.sort(key=lambda x: x.rank, reverse=True)
            league.findWinningTeam()

            context = {'results': league.lottery_results}
            return render(request, 'lottery_sim_results.html', context)

        except (json.JSONDecodeError, ValueError) as e:
            # Handle possible errors
            print(f"Error processing request: {e}")
            return HttpResponseBadRequest("Invalid data format or manager not found.")
    else:
        # Handle the case where cleaned_data is not provided
        return HttpResponseBadRequest("No data provided.")
