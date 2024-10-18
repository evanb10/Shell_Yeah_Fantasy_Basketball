from django.db import models

# Create your models here.
class Player(models.Model):
    player_id = models.CharField(max_length=50, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100,default='N/A')
    last_name = models.CharField(max_length=100,default='N/A')
    team = models.CharField(max_length=50, null=True)
    age = models.IntegerField(default=0)
    position = models.CharField(max_length=10,default='N/A')
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    # Add more fields as needed based on API response

    def __str__(self):
        return self.name
  
# class Manager(models.Model):
#   ''' Create Manager model that the database will be used to create the database.
#       Manager will house any and all necessary information about league managers. '''
#   manager_id = models.CharField(max_length=255,primary_key=True)
#   team_name = models.CharField(max_length=255,null=True)
#   display_name = models.CharField(max_length=255)
#   record = models.CharField(max_length=255,null=True)
#   wins = models.IntegerField(null=False,default=0)
#   losses = models.IntegerField(null=False,default=0)
#   points_for = models.IntegerField(null=False, default=0)
#   points_against = models.IntegerField(null=False, default=0)

#   def __repr__(self) -> str:
#       return self.__str__()

#   def __str__(self) -> str:
#       return self.display_name

# class Roster(models.Model):
#   ''' The roster table will house just the player ids and manager ids and will be used to track current fantasy rosters. '''
#   manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE, db_column='manager_id')
#   player_id = models.ForeignKey(Player, on_delete=models.CASCADE, db_column='player_id')

# class League(models.Model):
#    ''' The League table will house necesary information for the current season's league. '''
#    league_id = models.BigIntegerField(primary_key=True)
#    num_of_teams = models.IntegerField()
#    sport = models.CharField(max_length=25)
#    league_name = models.CharField(max_length=255)
#    previous_league_id = models.BigIntegerField()
#    year = models.IntegerField()

# class LeagueMembership(models.Model):
#   """
#   This model represents a membership of a Manager in a League.
#   """
#   manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
#   league = models.ForeignKey(League, on_delete=models.CASCADE)
#   # You can add additional fields specific to memberships here (e.g., joined_date, role)

#   class Meta:
#     unique_together = (('manager', 'league'),)  # Enforces unique manager-league combination


