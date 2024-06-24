from itertools import combinations
import random
from time import sleep
from collections import OrderedDict
import sqlite3

'''
1. Get team info which includes name, wins, losses, and standing at the end of last season (this is likely not even needed)
2. Find teams that have the same number of wins.  Sort each group into ascending order
3. Compare those teams' losses and sort them within each group.
4. Return the generated positions and compare them to the actual final standings.
5. If their the same good, if not then something needs to change. 

'''

class League:

    def __init__(self):
        # self.connection = sqlite3.connect('../../db.sqlite3')
        # self.db_cursor = self.connection.cursor()
        # self.name = self.get_league_name(league_id)
        self.teams = [] 
        self.total_teams = 0
        self.combinations = self.generate_combinations()
        self.lottery_results = {}
        
    def __repr__(self):
        for team in self.teams:
            print('*******************************')
            print(team)
            print('*******************************')
        return ''

    def addTeam(self,Team):
        self.teams.append(Team)
        self.total_teams+=1
    
    def generate_combinations(self):
        balls = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        combs = list(combinations(balls,4))
        for i in range(5):
            random.shuffle(combs)
        return combs[:-1]

    def getTeamInfo(self):
            name = input('Input Managers Name:\n')
            if name == 'exit':
                return 'exit'
            rank = input('Input Team\'s Final Ranking of Last Season:\n')
            wins = input('Input Team\'s Final Number of Wins Last Season:\n')
            losses = input('Input Team\'s Final Number of Losses Last Season:\n')
            # odds = input('Input the Odds This Team Will Win the First Overall Pick:\n')
            return Team(name,rank,wins,losses)   

    def splitCombinations(self):
        tempCombs = self.combinations
        for team in self.teams:
            team.combinations = tempCombs[:team.odds*10]
            tempCombs = list(set(tempCombs)-set(team.combinations))

    def oddsCheck(self):
        ''' Ensure that team odds all add up to 100 '''
        totalOdds = 0
        for team in self.teams:
            totalOdds += team.odds
        if totalOdds != 100:
            print(f'Odds must be equal to 100.  Current odds are {totalOdds}')
            exit(1)
        
    def combinationCheck(self):
        nextTeam = 1
        for team1 in self.teams[:-1]:
            for team2 in self.teams[nextTeam:]:
                intersectList = list(set(team1.combinations) & set(team2.combinations))
                if len(intersectList) != 0:
                    return intersectList
        print('There are no similar combinations')
                
    def sortTeamsDescend(self):
        return sorted(self.teams, key=lambda x: x.rank,reverse=True)
    
    def sortTeamsAscend(self):
        return sorted(self.teams, key=lambda x: x.rank)

    def generateWinningCombo(self):
        print(self.combinations)
        return random.choice(self.combinations)

    def findWinningTeam(self):
        for idx in range(3):
            if idx < 3 and len(self.combinations)>0:
                winningCombo = self.generateWinningCombo()
                for team in self.teams:
                    if winningCombo in team.combinations:
                        print(f'The number {idx+1} overall pick in the 2022 Fantasy Draft goes to...')
                        print(f'THE {team.rank} SEED TEAM! CONGRATS {team.name}!')
                        self.combinations = list(set(self.combinations)-set(team.combinations))
                        team.selected = True
                        self.lottery_results[idx+1] = team.name

        print('The remaining picks are ordered in reverse of season records. These are the results:\n')
        idx = 4
        for team in self.teams[::-1]:
            if team.selected == True:
                continue
            else:
                self.lottery_results[idx] = team.name
                idx += 1

    def returnRemainingTeam(self):
        pick = 4
        for team in self.teams:
            if team.selected == True:
                continue
            else:
                print(f'Pick {pick}: {team.name}')
            pick += 1
            sleep(1)

    def findTiedTeams(self):
        ''' findTiedTeams will loop through the list of teams and add each team to a dictionary where the key is the number of wins and the values are each teams with that number of wins '''
        wins_dict = {}
        # Loop through each team in the list
        for team in self.teams:
            # Add the team to the dictionary
            if team.wins in wins_dict:
                wins_dict[team.wins].append(team.name)
            else:
                wins_dict[team.wins] = [team.name]
        return wins_dict

    def sort_teams(self):
        '''Sorts fantasy basketball teams based on wins, losses, points for, and points against'''
        # Sort teams by wins (descending), then by losses (ascending), then by points for (descending),
        # and finally by points against (ascending)
        self.teams.sort(key=lambda x: (x.wins, -x.losses, x.points_for, x.points_against), reverse=True)
        for idx,team in enumerate(self.teams,start=1):
            team.rank = idx
    
    def setRanks(self):
        ''' Sets each teams rank after sorting by both wins and losses '''
        for idx,team in enumerate(reversed(self.teams),start=1):
            team.rank = idx

    def setOdds(self):
        ''' No longer needed as odds are already set by user through webpage '''
        for team in self.teams:
            team.positionalOdds()

    def splitOdds(self):
        ''' Split the odds for the teams that are tied in the lottery. '''
        combined_odds = 0
        tied_teams = []
        
        for idx,team in enumerate(self.teams[:-1],start=1):
            if team.rank <= 5 and (team.wins == self.teams[idx].wins) and (team.losses == self.teams[idx].losses):
                combined_odds += team.odds
                tied_teams.append(team)
                continue

            elif combined_odds > 0:
                combined_odds += team.odds
                tied_teams.append(team)
                if combined_odds % len(tied_teams) != 0:
                    for team_odds in tied_teams:
                        team_odds.odds = int(combined_odds // len(tied_teams))
                    random.choice(tied_teams).odds += 1
                else:
                    for team_odds in tied_teams:
                        team_odds.odds = int(combined_odds / len(tied_teams))
                
                tied_teams = []
                combined_odds = 0

    def sortOnLosses(self,team):
        return team.losses

    # def get_league_name(self, league_id):
    #     return self.db_cursor.execute('select league_name from lottery_sim_league where league_id == (?)', [league_id])
    #     # self.connection.commit()
        
class Team:
    # def __init__(self,name,rank,wins,losses):
    def __init__(self,name,odds,wins,losses,points_for,points_against):
        self.name = name
        self.rank = None 
        self.wins = wins
        self.losses = losses
        self.odds = odds 
        self.combinations = []
        self.selected = False
        self.points_for = points_for
        self.points_against = points_against

    def __repr__(self) -> str:
        return f'Team: {self.name}\nRank: {self.rank}\nWins: {self.wins}\nLosses: {self.losses}\nOdds: {self.odds}\nPoints For: {self.points_for}\nPoints Against: {self.points_against}\n'

    def positionalOdds(self):
        odds = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:10,
            9:15,
            10:20,
            11:25,
            12:30
        }
        self.odds = odds[self.rank]
    