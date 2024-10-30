from django.db import models

# Create your models here.
class Player(models.Model):
    player_id = models.CharField(max_length=50, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100,default='N/A')
    last_name = models.CharField(max_length=100,default='N/A')
    team = models.CharField(max_length=50, null=True)
    age = models.IntegerField(default=0,null=True)
    position = models.CharField(max_length=10,default='N/A',null=True)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    # Add more fields as needed based on API response

    def __str__(self):
      return f"{self.first_name} {self.last_name}"