import json
import sqlite3
import requests
import sys



class League():

    class Manager():
        def __init__(self, user_id, team_name, display_name, wins, losses) -> None:
            self.user_id = user_id
            self.team_name = team_name
            self.display_name = display_name
            self.wins = wins
            self.losses = losses

        def __repr__(self) -> str:
            return self.__str__()

        def __str__(self) -> str:
            return self.user_id+ ' : ' + self.display_name

    class Player():
        def __init__(self,firstname,lastname, age, team, id):
            self.firstname = firstname
            self.lastname = lastname
            self.team = team
            self.age = age
            self.id = id

        def __repr__(self) -> str:
            return self.__str__()

        def __str__(self) -> str:
            return self.firstname + ' ' + self.lastname

    def __init__(self):
        self.LEAGUE_ID = 1083085818937298944
        self.connection = sqlite3.connect('../../db.sqlite3')
        self.db_cursor = self.connection.cursor()
        self.players = []
        self.managers = []


    def add_player_to_league(self, first_name, last_name, age, team, id):
        player = self.Player(first_name, last_name, age, team, id)
        self.players.append(player)

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
  
    def get_rosters(self):
        league_id = self.LEAGUE_ID

        # Make the API call
        response = requests.get('https://api.sleeper.app/v1/league/{}/rosters'.format(league_id))

        # Check if the API call was successful
        if response.status_code == 200:
            # The API call was successful
            # Get the JSON response
            json_response = response.json()
            print(json_response)

            for roster in json_response:
                # print(roster)
                owner_id = roster['owner_id'] if roster['owner_id'] else 'test'
                players = roster['players'] if roster['players'] else []
                fpts = roster['settings']['fpts'] if roster['settings']['fpts'] else 0
                fpts_against = roster.get('settings').get('fpts_against') if roster.get('settings').get('fpts_against') else 0
                self.save_roster_to_database(owner_id, players, fpts, fpts_against)
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

    def get_managers(self):
        # Replace <league_id> with the ID of your Sleeper league
        league_id = self.LEAGUE_ID

        # Make the API call
        response = requests.get('https://api.sleeper.app/v1/league/{}/users'.format(league_id))

        # Check if the API call was successful
        if response.status_code == 200:
            # The API call was successful
            # Get the JSON response
            json_response = response.json()

            for manager in json_response:
                man = self.Manager(manager['user_id'], manager['metadata']['team_name'] if 'team_name' in manager['metadata'] else None, manager['display_name'], manager['metadata']['wins'] if 'wins' in manager['metadata'] else 0, manager['metadata']['wins'] if 'wins' in manager['metadata'] else 0)
                print(man)
                #print(manager)
                self.managers.append(man)
#                manager_arr = [user['user_id'], user['display_name']]
#                print(manager_arr)
#                if 'team_name' in manager['metadata']:
#                    manager_arr.append(user['metadata']['team_name'])
#                managers.append(user_arr)
        else:
            # The API call failed
            print('API call failed with status code {}'.format(response.status_code))


    def get_players_api(self):

        # Make the API call
        response = requests.get('https://api.sleeper.app/v1/players/nba')

        # Check if the API call was successful
        if response.status_code == 200:
            # The API call was successful
            # Get the JSON response
            json_response = response.json()
            players = self.remove_letter_keys(json_response)
            for player in players:
                id = player
                #player = player.value()
                self.add_player_to_league(players[id]['first_name'], players[id]['last_name'], players[id]['age'], players[id]['team'], id)

        else:
            # The API call failed
            print('API call failed with status code {}'.format(response.status_code))

    def get_league_api(self):
        response = requests.get(f'https://api.sleeper.app/v1/league/{self.LEAGUE_ID}')
        # Check if the API call was successful
        if response.status_code == 200:
            # The API call was successful
            # Get the JSON response
            json_response = response.json()
            num_rosters = json_response['total_rosters']
            league_id = json_response['league_id']
            sport = json_response['sport']
            league_name = json_response['name']
            previous_league_id = json_response['previous_league_id']
            year = json_response['season']
            self.db_cursor.execute('insert into lottery_sim_league (league_id, num_of_teams, sport, league_name, previous_league_id, year) values (?,?,?,?,?,?)',[league_id, num_rosters, sport, league_name, previous_league_id, year])
            self.connection.commit()

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
        for player in league.players:
            self.db_cursor.execute('insert into lottery_sim_player (firstname,lastname,age,team,player_id) values (?,?,?,?,?)',[player.firstname,player.lastname,player.age,player.team,player.id])
        self.connection.commit()

    def clear_players_table(self):
        self.db_cursor.execute('delete from lottery_sim_player')
        self.connection.commit()

    def save_managers_to_database(self):
        print('SAVING')
        for manager in league.managers:
            self.db_cursor.execute('insert into lottery_sim_manager(manager_id,team_name,display_name,league_id, wins, losses, points_for, points_against) values (?,?,?,?,?,?,?,?)',[manager.user_id, manager.team_name, manager.display_name, league.LEAGUE_ID, manager.wins, manager.losses, 0, 0])
        self.connection.commit()

    def clear_managers_table(self):
        self.db_cursor.execute('delete from lottery_sim_manager')
        self.connection.commit()

    def save_league_to_database(self):
        self.db_cursor.execute('insert into lottery_sim_league')


# Main Section
opts = sys.argv
league = League()

if '--update-players' in opts:
    # Pull updated player info from Sleeper and write to file
    league.get_players_api()
    league.clear_players_table()
    league.save_players_to_database()

if '--update-man' in opts:
    league.get_managers()
    league.clear_managers_table()
    league.save_managers_to_database()

if '--update-rosters' in opts:
    league.get_rosters()

if '--update-league' in opts:
    league.get_league_api()

if '--update-all' in opts:
    #Update players
    league.get_players_api()
    league.clear_players_table()
    league.save_players_to_database()

    #Update managers
    league.get_managers()
    league.clear_managers_table()
    league.save_managers_to_database()

    #Update rosters
    league.get_rosters()

if '--help' in opts or len(opts) == 1:
    print('''
            This script is used to update the local database with data from Sleeper\'s API.
            To update the players database: "python3 fantasy_analytics.py --update-players"
            To update the managers database: "python3 fantasy_analytics.py --update-man"
            To update the rosters database: "python3 fantasy_analytics.py --update-rosters"
            Provide any combination of the above to update desired content. 

            Additionally, if updates to all tables is desired: "python3 fantasy_analytics.py --update-all"
        ''')
