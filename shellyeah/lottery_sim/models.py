from django.db import models

# Create your models here.
class Player(models.Model):
  ''' Create Player model that the database will be used to create the database.
      Player will house any and all necessary information for the entirety of the project. '''
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  age= models.IntegerField(blank=True, null=True)
  team = models.CharField(max_length=255,blank=True, null=True)
  player_id = models.IntegerField(primary_key=True)
  
class Manager(models.Model):
  ''' Create Manager model that the database will be used to create the database.
      Manager will house any and all necessary information about league managers. '''
  manager_id = models.CharField(max_length=255,primary_key=True)
  team_name = models.CharField(max_length=255,null=True)
  display_name = models.CharField(max_length=255)
  record = models.CharField(max_length=255,null=True)
  league_id = models.ForeignKey("League",on_delete=models.CASCADE,db_column='league_id')
  wins = models.IntegerField(null=False,default=0)
  losses = models.IntegerField(null=False,default=0)
  points_for = models.IntegerField(null=False, default=0)
  points_against = models.IntegerField(null=False, default=0)

  def __repr__(self) -> str:
      return self.__str__()

  def __str__(self) -> str:
      return self.display_name

class Roster(models.Model):
  ''' The roster table will house just the player ids and manager ids and will be used to track current fantasy rosters. '''
  manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE, db_column='manager_id')
  player_id = models.ForeignKey(Player, on_delete=models.CASCADE, db_column='player_id')

class League(models.Model):
   ''' The League table will house necesary information for the current season's league. '''
   league_id = models.BigIntegerField(primary_key=True)
   num_of_teams = models.IntegerField()
   sport = models.CharField(max_length=25)
   league_name = models.CharField(max_length=255)
   previous_league_id = models.BigIntegerField()
   year = models.IntegerField()


