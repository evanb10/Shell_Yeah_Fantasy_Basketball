import json
import sqlite3
import sys
import argparse

import os
import django
import requests


import os
import django
import requests


project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','shellyeah.settings')
django.setup()

from players.models import Player
from lottery_sim.models import Manager



def remove_letter_keys(self, my_dict):
    """Removes all items from a dictionary if the key has letters.

    Args:
        my_dict: The dictionary to modify.

    Returns:
        The modified dictionary with keys containing letters removed.
    """
    # Create an empty dictionary to store remaining items
    filtered_dict = {}
    
    # Loop through each key-value pair in the original dictionary
    for key, value in my_dict.items():
        # Check if the key is a string and contains at least one letter
        if isinstance(key, str) and any(char.isalpha() for char in key):
            # Skip keys with letters
            continue
        # If it's not a string with letters, add it to the new dictionary
        filtered_dict[key] = value
    
    # Clear the original dictionary (modifying it in-place)
    my_dict.clear()
    
    # Update the original dictionary with the filtered items
    my_dict.update(filtered_dict)
    
    # Return the modified dictionary
    return my_dict

def get_rosters(league_id):

    # Make the API call
    response = requests.get('https://api.sleeper.app/v1/league/{}/rosters'.format(league_id))

    # Check if the API call was successful
    if response.status_code == 200:
        # The API call was successful
        # Get the JSON response
        json_response = response.json()
        # print(json_response)

        for roster in json_response:
            # print(roster)
            owner_id = roster['owner_id'] if roster['owner_id'] else 'test'
            players = roster['players'] if roster['players'] else []
            fpts = roster['settings']['fpts'] if roster['settings']['fpts'] else 0
            fpts_against = roster.get('settings').get('fpts_against') if roster.get('settings').get('fpts_against') else 0
            save_roster_to_database(owner_id, players, fpts, fpts_against)
            #man = self.Manager(manager['user_id'], manager['metadata']['team_name'] if 'team_name' in manager['metadata'] else None, manager['display_name'])
            #self.managers.append(man)
#                manager_arr = [user['user_id'], user['display_name']]
#                print(manager_arr)
#                if 'team_name' in manager['metadata']:
#                    manager_arr.append(user['metadata']['team_name'])
#                managers.append(user_arr)
    else:
        # The API call failed
        print('API call failed with status code {}'.format(response.status_code))

# def get_players_api(self):

#     # Make the API call
#     response = requests.get('https://api.sleeper.app/v1/players/nba')

#     # Check if the API call was successful
#     if response.status_code == 200:
#         # The API call was successful
#         # Get the JSON response
#         json_response = response.json()
#         players = self.remove_letter_keys(json_response)
#         for player in players:
#             id = player
#             add_player_to_league(
#                 players[id]['first_name'], 
#                 players[id]['last_name'], 
#                 players[id]['age'],
#                 players[id]['weight'],
#                 players[id]['height'], 
#                 players[id]['position'], 
#                 players[id]['team'], 
#                 id
#                 )

#     else:
#         # The API call failed
#         print('API call failed with status code {}'.format(response.status_code))
def get_prev_league_api(prev_id):
    response_rosters = requests.get('https://api.sleeper.app/v1/league/{}/rosters'.format(prev_id))
    response_users = requests.get('https://api.sleeper.app/v1/league/{}/users'.format(prev_id))

    from collections import defaultdict

    # Initialize a dictionary with a nested structure for wins and losses.
    results = defaultdict(lambda: {"user_name": "", "wins": 0, "losses": 0, "pf": 0, "pa": 0})
    # print(response_users.json())
    users_dict = {user['user_id'] : user for user in response_users.json()}

    # Loop through each record
    for record in response_rosters.json():
        owner_id = record['owner_id']
        results[owner_id]["user_name"] = users_dict[owner_id]['display_name']
        results[owner_id]["wins"] = record["settings"]['wins']
        results[owner_id]["losses"] = record["settings"]['losses']
        results[owner_id]["pf"] = record["settings"]['fpts']
        results[owner_id]["pa"] = record["settings"]['fpts_against']

    # Convert defaultdict to a regular dict for returning
    return dict(results)

def get_league_api(league_id):
    # Fetch league data from API
    response = requests.get('https://api.sleeper.app/v1/league/{}'.format(league_id))
    

    # Check for successful response
    if response.status_code == 200:
        json_response = response.json()

        # Extract league information
        num_rosters = json_response['total_rosters']
        league_id = json_response['league_id']
        sport = json_response['sport']
        league_name = json_response['name']
        previous_league_id = json_response['previous_league_id']
        year = json_response['season']

        # print(json_response)

        # # Check if league already exists (using SELECT statement)
        # exists_stmt = "SELECT 1 FROM lottery_sim_league WHERE league_id=?"
        # self.db_cursor.execute(exists_stmt, (league_id,))

        # # Check if any results exist (league exists if results exist)
        # exists = self.db_cursor.fetchone() is not None

        # if exists:
        #     # Update existing league
        #     update_stmt = """
        #         UPDATE lottery_sim_league
        #         SET num_of_teams=?, sport=?, league_name=?, previous_league_id=?, year=?
        #         WHERE league_id=?
        #     """
        #     self.db_cursor.execute(update_stmt, (num_rosters, sport, league_name, previous_league_id, year, league_id))
        # else:
        #     # Insert new league
        #     self.db_cursor.execute('insert into lottery_sim_league (league_id, num_of_teams, sport, league_name, previous_league_id, year) values (?,?,?,?,?,?)',
        #                             [league_id, num_rosters, sport, league_name, previous_league_id, year])
        # self.connection.commit()


def save_roster_to_database(self, owner_id, roster, points_for, points_against):
    print('SAVING')
    for player in roster:
        self.db_cursor.execute('insert into lottery_sim_roster (manager_id, player_id) values (?,?)',[owner_id, player])
        self.db_cursor.execute('UPDATE lottery_sim_manager SET points_for = ?, points_against = ? WHERE manager_id = ?', [points_for, points_against, owner_id])

    self.connection.commit()

def clear_roster_table(self):
    self.db_cursor.execute('delete from lottery_sim_roster')
    self.connection.commit()

def save_players_to_database(self):
    print('SAVING')
    for player in self.players:
        print(player)
        Player.objects.update_or_create(
            player_id = player.player_id,
            defaults = {
                'first_name' : player.first_name,
                'last_name' : player.last_name,
                'age' : player.age,
                'weight' : player.weight,
                'height' : player.height,
                'position' : player.position,
                'team' : player.team,
            }
        )
        # self.db_cursor.execute('insert into players_player (first_name,last_name,age,weight,height,position,team,player_id) values (?,?,?,?,?,?,?,?)',[player.firstname,player.lastname,player.age,player.weight,player.height,player.position,player.team,player.id])
    # self.connection.commit()

def clear_players_table(self):
    print(self.db_cursor.fetchall())

    self.db_cursor.execute('delete from players_player')
    self.connection.commit()

def user_to_leagues(user_name):
    
    leagues = []

    response_user_name = requests.get('https://api.sleeper.app/v1/user/{}'.format(user_name))

    if response_user_name.status_code == 200:
        json_response_user = response_user_name.json()

    user_id = json_response_user['user_id']

    response_leagues = requests.get('https://api.sleeper.app/v1/user/{}/leagues/nba/{}'.format(user_id,str(2024)))
    for league in response_leagues.json():
        temp = {'avatar':league['avatar'], 'league_id':league['league_id'], 'previous_league_id':league['previous_league_id'], 'name':league['name'],}
        leagues.append(temp)
    # print(response_leagues.json())
    return leagues

def update_managers(league_id):
    # Replace <league_id> with the ID of your Sleeper league

    # Make the API call
    response_users = requests.get('https://api.sleeper.app/v1/league/{}/users'.format(league_id))
    response_rosters = requests.get('https://api.sleeper.app/v1/league/{}/rosters'.format(league_id))

    

    # Check if the API call was successful
    if response_users.status_code == 200:
        if response_rosters.status_code == 200:

            rosters_dict = {roster['owner_id'] : roster for roster in response_rosters.json()}

            # The API call was successful
            # Get the JSON response
            json_response_users = response_users.json()

            # For each manager in json response, update or create a new entry in the table using manager and roster data
            for manager in json_response_users:
                manager_id_temp = manager['user_id']
                Manager.objects.update_or_create(
                    manager_id = manager_id_temp,
                    league_id = manager['league_id'],
                    defaults = {
                        "team_name" : manager['metadata']['team_name'] if 'team_name' in manager['metadata'] else None, 
                        "display_name" : manager['display_name'], 
                        "record" : rosters_dict[manager_id_temp]['metadata']['record'],
                        'wins' : rosters_dict[manager_id_temp]['settings']['wins'],
                        'losses' : rosters_dict[manager_id_temp]['settings']['losses'],
                        'points_for' : rosters_dict[manager_id_temp]['settings']['fpts'],
                        'points_against' : rosters_dict[manager_id_temp]['settings']['fpts_against'],
                        'roster' : {'players':rosters_dict[manager_id_temp]['players'],'ir':rosters_dict[manager_id_temp]['reserve']}
                    },
                )
            
        else:
            # The API call failed
            print('API call failed with status code {}'.format(response_rosters.status_code))

    

    else:
        # The API call failed
        print('API call failed with status code {}'.format(response_users.status_code))


def save_managers_to_database(self):
    for manager in self.managers:
        # Check if manager exists in the specified league
        exists_in_league_stmt = """
            SELECT 1
            FROM lottery_sim_leaguemembership lm
            INNER JOIN lottery_sim_manager m ON lm.manager_id = m.manager_id
            WHERE lm.league_id = ? AND m.manager_id = ?
        """
        self.db_cursor.execute(exists_in_league_stmt, (self.LEAGUE_ID, manager.user_id))
        exists_in_league = self.db_cursor.fetchone() is not None

        if exists_in_league:
            # Update existing manager in Manager table
            update_manager_stmt = """
                UPDATE lottery_sim_manager
                SET team_name = ?, display_name = ?, wins = ?, losses = ?, points_for = ?, points_against = ?
                WHERE manager_id = ?
            """
            self.db_cursor.execute(update_manager_stmt, 
                (manager.team_name, manager.display_name, manager.wins, manager.losses, 0, 0, manager.user_id))
        else:
            # Check if manager exists in Manager table
            exists_stmt = "SELECT 1 FROM lottery_sim_manager WHERE manager_id = ?"
            self.db_cursor.execute(exists_stmt, (manager.user_id,))
            exists = self.db_cursor.fetchone() is not None

            if not exists:
                # Insert new manager into Manager table
                insert_manager_stmt = """
                    INSERT INTO lottery_sim_manager (manager_id, team_name, display_name, wins, losses, points_for, points_against)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                self.db_cursor.execute(insert_manager_stmt, 
                    (manager.user_id, manager.team_name, manager.display_name, manager.wins, manager.losses, 0, 0))

            # Insert into League Membership table if not exists
            insert_membership_stmt = """
                INSERT INTO lottery_sim_leaguemembership (manager_id, league_id)
                VALUES (?, ?)
            """
            self.db_cursor.execute(insert_membership_stmt, (manager.user_id, self.LEAGUE_ID))
    
    self.connection.commit()


def clear_managers_table(self):
    self.db_cursor.execute('delete from lottery_sim_manager')
    self.connection.commit()

def save_league_to_database(self):
    self.db_cursor.execute('insert into lottery_sim_league')


# Main Section
# opts = sys.argv
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse command line arguments for sleeper.py")
    parser.add_argument("--update_players", dest='update_players',  action="store_true", help="Used to update players in the database")
    parser.add_argument("--update_man", dest='update_man',  action="store_true", help="")
    parser.add_argument("--update_rosters", dest='update_rosters',  action="store_true", help="Used to update rosters in the database")
    parser.add_argument("--update_league", dest='update_league',  action="store_true", help="Used to update the league info in the database")
    parser.add_argument("--update_all", dest='update_all',  action="store_true", help="Used to update all information in the database")
    parser.add_argument("--league_id", dest='league_id',  action="store_true", help="Get the league id that the user would like to update")
    # parser.add_argument("--show-help", action="store_true", dest="show_help", help="Display help message")

    args = parser.parse_args()
    print(vars(args))
    # print(any(not getattr(args, attr) for attr in vars(args) if attr != '_help'))
    # print(vars(args))
    # if len(vars(args)) == 1 or any(not getattr(args, attr) for attr in vars(args) if attr != 'show_help'):
    #     print('user needs help')
    #     parser.print_help()
    # else:
    league = League(args.league_id) if args.league_id else League()

    if args.update_players:
    # Pull updated player info from Ssleeper and write to file
        league.get_players_api()
        # league.clear_players_table()
        league.save_players_to_database()

    if args.update_man:
        league.get_managers()
        league.clear_managers_table()
        league.save_managers_to_database()

    if args.update_rosters:
        league.get_rosters()

    if args.update_league:
        league.get_league_api()

    if args.update_all:
    #Update players
        league.get_players_api()
        league.clear_players_table()
        league.save_players_to_database()

        #Update managers
        get_managers()
        clear_managers_table()
        save_managers_to_database()

        #Update rosters
        get_rosters()
