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
        return random.choice(self.combinations)

    def findWinningTeam(self):
        for idx in range(3):
            if idx < 3:
                print('SELECTING LOTTERY TEAM')
                winningCombo = self.generateWinningCombo()
                print(winningCombo)
                print(len(self.combinations))
                for team in self.teams:
                    if winningCombo in team.combinations:
                        print(len(team.combinations))
                        print(f'The number {idx+1} overall pick in the 2022 Fantasy Draft goes to...')
                        # sleep(2)
                        print(f'THE {team.rank} SEED TEAM! CONGRATS {team.name}!')
                        self.combinations = list(set(self.combinations)-set(team.combinations))
                        team.selected = True
                        self.lottery_results[idx+1] = team.name

        print('The remaining picks are ordered in reverse of season records. These are the results:\n')
        idx = 4
        for team in self.teams[::-1]:
            print(idx)
            if team.selected == True:
                continue
            else:
                print(f'Pick {idx}: {team.name}')
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
        
    # def sortTeams(self,wins_dict):
    #     ''' Loops through the wins_dict and sorts each based on losses.  Corrects for possible ties.  Team with tie should be ranked higher than others '''
    #     sorted_teams = []
    #     print('WINS DICT' , wins_dict)
    #     wins_dict = OrderedDict(sorted(wins_dict.items()))

    #     for num_wins, team_list in wins_dict.items():
    #         if len(team_list) > 1:
    #             #decide by losses
    #             #sorted_teams.append()
    #             temp_teams = [team for team in self.teams if team.name in team_list]
    #             temp_teams.sort(key= lambda x: x.losses,reverse=True)
    #             sorted_teams = [ *sorted_teams, *temp_teams ] 
    #         else:
    #             sorted_teams.append(*[team for team in self.teams if team.name==team_list[0]])
    #     self.teams = sorted_teams

    # def sortTeams(self, wins_dict):
    #     '''Sorts fantasy basketball teams based on wins and losses, with tiebreaker'''
    #     sorted_teams = []

    #     # Sort the wins_dict by number of wins
    #     wins_dict = OrderedDict(sorted(wins_dict.items()))

    #     for num_wins, team_list in wins_dict.items():
    #         teams_with_num_wins = [team for team in self.teams if team.name in team_list]
    #         # Sort teams by wins (descending)
    #         teams_with_num_wins.sort(key=lambda x: x.wins, reverse=True)
    #         # Then sort teams within the same number of wins by losses (ascending)
    #         teams_with_num_wins.sort(key=lambda x: x.losses)
    #         # Then sort teams within the same number of wins and losses by points for (descending)
    #         teams_with_num_wins.sort(key=lambda x: x.points_for, reverse=True)
    #         # Finally, sort teams within the same number of wins, losses, and points for by points against (ascending)
    #         teams_with_num_wins.sort(key=lambda x: x.points_against)

    #         sorted_teams.extend(teams_with_num_wins)

    #     self.teams = sorted_teams

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
            #print(f'TEAM: {team}')
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
                # print(f'{team} \n\n IS EQUAL TO \n\n {self.teams[idx]}')
                continue

            elif combined_odds > 0:
                combined_odds += team.odds
                tied_teams.append(team)
                # print(f'combined odds of previous teams: {combined_odds}')
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
    #     return self.db_cursor.execute('select league_name from fantasy_basketball_league where league_id == (?)', [league_id])
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
    
def main():
    league = League('test')

    # team12 = Team('Zach',12,1,20)
    # team11 = Team('Evan',11,6,15)
    # team10 = Team('Nik',10,6,15)
    # team9 = Team('Mikey',9,6,13)
    # team8 = Team('PJ',8,8,13)
    # team7 = Team('Nimesh',7,9,12)
    # team6 = Team('JJ',6,10,11)
    # team5 = Team('James',5,12,9)
    # team4 = Team('Tony',4,14,6)
    # team3 = Team('Dylan',3,16,5)
    # team2 = Team('Barbone',2,17,4)
    # team1 = Team('Rocco',1,19,2)
    team12 = Team('Zach',1,20)
    team11 = Team('Evan',6,15)
    team10 = Team('Nik',6,15)
    team9 = Team('Mikey',7,13)
    team8 = Team('PJ',10,14)
    team7 = Team('Nimesh',9,15)
    team6 = Team('JJ',11,13)
    team5 = Team('James',14,10)
    team4 = Team('Tony',15,8)
    team3 = Team('Dylan',19,6)
    team2 = Team('Barbone',18,6)
    team1 = Team('Rocco',22,2)
    league.teams = [team7,team6,team9,team12,team8,team5,team4,team11,team10,team3,team2,team1]

#    print('When there are no managers left to add, type \'exit\'')
#    while True:
#        team = league.getTeamInfo()
#        if team == 'exit':
#            break
#        else:
#            league.addTeam(team)
#    for team in league.teams:
 #       print('*******************************')
  #      print(team)
   #     print('*******************************')
    #for i in range(3):
     #   print('\n')
    wins_dict = league.findTiedTeams()
    #for team in league.teams:
     #   print('*******************************')
      #  print(team)
       # print('*******************************')
    league.sortTeams(wins_dict)
    league.setRanks()
    league.setOdds()
    league.splitOdds()
    #print(league)
    league.oddsCheck()
    league.splitCombinations()
    #league.combinationCheck()
    league.teams.sort(key = lambda x: x.rank,reverse=True)
#    for i in range(3):
#        league.findWinningTeam(i)
#    print('The remaining picks are ordered in reverse of season records. These are the results:\n')

#    pick = 4
#    for team in league.teams:
#        if team.selected == True:
#            continue
#        else:
#            print(f'Pick {pick}: {team.name}')
#            pick += 1
 #       sleep(1)








#
# def main():
#    input("Welcome to the 2022 Turt Fantasy Draft\nPress 'Enter' to begin...\n")

#    combinations = generate_combinations()
#    team12 = Team('Evan',12,combinations[:300])
#    team11 = Team('Zach',11,combinations[300:550])
#    team10 = Team('Nik',10,combinations[550:750])
#    team9 = Team('Nimesh',9,combinations[750:900])
#    team8 = Team('Barbone',8,combinations[900:1000])
#    team7 = Team('Mikey',7,[])
#    team6 = Team('James',6,[])
#    team5 = Team('JJ',5,[])
#    team4 = Team('Tony',4,[])
#    team3 = Team('PJ',3,[])
#    team2 = Team('Rocco',2,[])
#    team1 = Team('Dylan',1,[])
#    teams = [team12,team11,team10,team9,team8,team7,team6,team5,team4,team3,team2,team1]
#    for i in range(3):
#        rand_comb = random.choice(combinations)

#        if rand_comb in team12.combinations:
#            print(f'The number {i+1} overall pick in the 2022 Fantasy Turts Draft goes to...')
#            sleep(2)
#            print(f'THE 12th SEED TEAM! CONGRATS {team12.name}!')
#            combinations = list(set(combinations)-set(team12.combinations))
#            team12.selected = True
#        elif rand_comb in team11.combinations:
#            print(f'The number {i+1} overall pick in the 2022 Fantasy Turts Draft goes to...')
#            sleep(2)
#            print(f'THE 11th SEED TEAM! CONGRATS {team11.name}!')
#            combinations = list(set(combinations)-set(team11.combinations))
#            team11.selected = True
#        elif rand_comb in team10.combinations:
#            print(f'The number {i+1} overall pick in the 2022 Fantasy Turts Draft goes to...')
#            sleep(2)
#            print(f'THE 10th SEED TEAM! CONGRATS {team10.name}!')
#            combinations = list(set(combinations)-set(team10.combinations))
#            team10.selected = True
#        elif rand_comb in team9.combinations:
#            print(f'The number {i+1} overall pick in the 2022 Fantasy Turts Draft goes to...')
#            sleep(2)
#            print(f'THE 9th SEED TEAM! CONGRATS {team9.name}!')
#            combinations = list(set(combinations)-set(team9.combinations))
#            team9.selected = True
#        elif rand_comb in team8.combinations:
#            print(f'The number {i+1} overall pick in the 2022 Fantasy Turts Draft goes to...')
#            sleep(2)
#            print(f'THE 8th SEED TEAM! CONGRATS {team8.name}!')
#            combinations = list(set(combinations)-set(team8.combinations))
#            team8.selected = True 
#        input()
   
#    print('The remaining picks are ordered in reverse of season records. These are the results:\n')
#    pick = 4
#    for team in teams:
#        if team.selected == True:
#            continue
#        else:
#            print(f'Pick {pick}: {team.name}')
#        pick += 1
#        sleep(3)


# if __name__ == '__main__':
#     main()
