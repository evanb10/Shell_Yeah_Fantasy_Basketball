# players/management/commands/import_players.py
import json
import requests
from django.core.management.base import BaseCommand
from lottery_sim.models import Player

class Command(BaseCommand):
    help = 'Fetch players from Sleeper API and save to database'

    def handle(self, *args, **kwargs):
        # URL for the Sleeper API endpoint
        url = 'https://api.sleeper.app/v1/players/nba'  # Replace with actual endpoint
        response = requests.get(url)

        if response.status_code == 200:
            player_data = self.remove_letter_keys(response.json())

            with open('players.json','w') as f:
                json.dump(player_data,f)


            # Assuming player_data is a dictionary of players, where each key is a player ID
            for player_id, player_info in player_data.items():
                # Extract relevant information from player_info
                first_name = player_info.get('first_name') if 'first_name' in player_info  and player_info['first_name'] != None else 'N/A'
                last_name = player_info.get('last_name') if 'last_name' in player_info  and player_info['last_name'] != None else 'N/A'
                team = player_info.get('team') if 'team' in player_info  and player_info['team'] != None else 'N/A'
                age = player_info.get('age') if 'age' in player_info and player_info['age'] != None else 0
                position = player_info.get('position') if 'position' in player_info  and player_info['position'] != None else 'N/A'
                weight = player_info.get('weight') if 'weight' in player_info  and player_info['weight'] != None else 0
                height = player_info.get('height') if 'height' in player_info  and player_info['height'] != None else 0

                if not(first_name) or not(last_name) or not(team) or not(age) or not(position) or not(weight) or not(height):
                    print(player_id)

                # Save or update the player in the database
                Player.objects.update_or_create(
                    player_id=player_id,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'team': team,
                        'age': age,
                        'position': position,
                        'weight': weight,
                        'height': height,
                    }
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(player_data)} players.'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data from Sleeper API.'))

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
    
    def inches_to_feet_and_inches(total_inches):
        """Converts a given number of inches to feet and inches.

        Args:
            total_inches: The total number of inches to convert.

        Returns:
            A tuple containing the number of feet and inches.
        """

        feet = total_inches // 12
        inches = total_inches % 12
        return feet, inches