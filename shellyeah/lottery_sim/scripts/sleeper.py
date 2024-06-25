import json
import sqlite3
import requests
import sys
import argparse



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
            # + '\nTeam_name: ' + self.team_name 
            return 'User_id: ' + str(self.user_id) + '\tDisplay_name: ' + self.display_name + '\n' #+ '\nWins: ' + str(self.wins) + '\nLosses' + str(self.losses)

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

    def __init__(self, league_id):
        self.LEAGUE_ID = league_id
        self.connection = sqlite3.connect('db.sqlite3')
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
                # print('\n'*2)

                # print(f'user id: {manager["user_id"]}')
                # print(f'team_name: {manager["metadata"]["team_name"]}')
                # print(f'display_name: {manager["display_name"]}')
                man = self.Manager(manager['user_id'], manager['metadata']['team_name'] if 'team_name' in manager['metadata'] else None, manager['display_name'], manager['metadata']['wins'] if 'wins' in manager['metadata'] else 0, manager['metadata']['wins'] if 'wins' in manager['metadata'] else 0)
                #print(manager)
                # print(manager)
                # print('\n'*2)
                self.managers.append(man)
#                manager_arr = [user['user_id'], user['display_name']]
#                print(manager_arr)
#                if 'team_name' in manager['metadata']:
#                    manager_arr.append(user['metadata']['team_name'])
#                managers.append(user_arr)
            print('*'*50)
            print(self.managers)
            print('*'*50)

            
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
        # Fetch league data from API
        response = requests.get(f'https://api.sleeper.app/v1/league/{self.LEAGUE_ID}')

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

            # Check if league already exists (using SELECT statement)
            exists_stmt = "SELECT 1 FROM lottery_sim_league WHERE league_id=?"
            self.db_cursor.execute(exists_stmt, (league_id,))

            # Check if any results exist (league exists if results exist)
            exists = self.db_cursor.fetchone() is not None

            if exists:
                # Update existing league
                update_stmt = """
                    UPDATE lottery_sim_league
                    SET num_of_teams=?, sport=?, league_name=?, previous_league_id=?, year=?
                    WHERE league_id=?
                """
                self.db_cursor.execute(update_stmt, (num_rosters, sport, league_name, previous_league_id, year, league_id))
            else:
                # Insert new league
                self.db_cursor.execute('insert into lottery_sim_league (league_id, num_of_teams, sport, league_name, previous_league_id, year) values (?,?,?,?,?,?)',
                                        [league_id, num_rosters, sport, league_name, previous_league_id, year])
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
        for player in self.players:
            self.db_cursor.execute('insert into lottery_sim_player (firstname,lastname,age,team,player_id) values (?,?,?,?,?)',[player.firstname,player.lastname,player.age,player.team,player.id])
        self.connection.commit()

    def clear_players_table(self):
        self.db_cursor.execute('delete from lottery_sim_player')
        self.connection.commit()

    def save_managers_to_database(self):
        for manager in self.managers:
            # Check if manager exists using a SELECT statement
            exists_stmt = """
                SELECT 1
                FROM lottery_sim_leaguemembership lm
                INNER JOIN lottery_sim_manager m ON lm.manager_id = m.manager_id
                WHERE lm.league_id = ? AND m.manager_id = ?
            """
            self.db_cursor.execute(exists_stmt, (manager.user_id, self.LEAGUE_ID))

            # Fetch results (should be empty or single row)
            exists = self.db_cursor.fetchone() is not None

            if exists:
            # Update existing manager in Manager table
                update_manager_stmt = """
                    UPDATE lottery_sim_manager
                    SET team_name=?, display_name=?, wins=?, losses=?, points_for=?, points_against=?
                    WHERE manager_id=?
                """
                self.db_cursor.execute(update_manager_stmt, (manager.team_name, manager.display_name, manager.wins, manager.losses, 0, 0, manager.user_id))
            else:
                exists_stmt = "SELECT 1 FROM lottery_sim_manager WHERE manager_id = ?"
                self.db_cursor.execute(exists_stmt, (manager.user_id,))

                # Fetch results (should be empty or single row)
                exists = self.db_cursor.fetchone() is not None

                if not exists:
                    # Insert new manager into both tables
                    insert_manager_stmt = """
                        INSERT INTO lottery_sim_manager (manager_id, team_name, display_name, wins, losses, points_for, points_against)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    self.db_cursor.execute(insert_manager_stmt, (manager.user_id, manager.team_name, manager.display_name, manager.wins, manager.losses, 0, 0))
                
                exists_stmt = "SELECT 1 FROM lottery_sim_leaguemembership WHERE manager_id = ? AND league_id = ?"
                self.db_cursor.execute(exists_stmt, (manager.user_id,self.LEAGUE_ID,))

                # Fetch results (should be empty or single row)
                exists = self.db_cursor.fetchone() is not None

                if not exists:
                # Insert new league membership
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
#opts = sys.argv
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Parse command line arguments for sleeper.py")
#     parser.add_argument("--update_players", dest='update_players', type=str, help="Used to update players in the database")
#     parser.add_argument("--update_man", dest='update_man', type=str, help="")
#     parser.add_argument("--update_rosters", dest='update_rosters', type=str, help="Used to update rosters in the database")
#     parser.add_argument("--update_league", dest='update_league', type=str, help="Used to update the league info in the database")
#     parser.add_argument("--update_all", dest='update_all', type=str, help="Used to update all information in the database")
#     parser.add_argument("--league_id", dest='league_id', type=str, help="Get the league id that the user would like to update")

#     args = parser.parse_args()
#     league = League(args.league_id)

#     if args.update_players:
#         # Pull updated player info from Sleeper and write to file
#         league.get_players_api()
#         league.clear_players_table()
#         league.save_players_to_database()

#     if args.update_man:
#         league.get_managers()
#         league.clear_managers_table()
#         league.save_managers_to_database()

#     if args.update_rosters:
#         league.get_rosters()

#     if args.update_league:
#         league.get_league_api()

#     if args.update_all:
#         #Update players
#         league.get_players_api()
#         league.clear_players_table()
#         league.save_players_to_database()

#         #Update managers
#         league.get_managers()
#         league.clear_managers_table()
#         league.save_managers_to_database()

#         #Update rosters
#         league.get_rosters()

#     if args.help or len(args) == 1:
#         print('''
#                 This script is used to update the local database with data from Sleeper\'s API.
#                 To update the players database: "python3 fantasy_analytics.py --update-players"
#                 To update the managers database: "python3 fantasy_analytics.py --update-man"
#                 To update the rosters database: "python3 fantasy_analytics.py --update-rosters"
#                 Provide any combination of the above to update desired content. 

#                 Additionally, if updates to all tables is desired: "python3 fantasy_analytics.py --update-all"
#             ''')
