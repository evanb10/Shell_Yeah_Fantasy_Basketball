class Team:
    def __init__(self, name, wins, losses, points_for, points_against):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.points_for = points_for
        self.points_against = points_against

class FantasyBasketballManager:
    def sort_teams(self, teams):
        '''Sorts fantasy basketball teams based on wins, losses, points for, and points against'''
        # Sort teams by wins (descending), then by losses (ascending), then by points for (descending),
        # and finally by points against (ascending)
        teams.sort(key=lambda x: (x.wins, -x.losses, x.points_for, x.points_against), reverse=True)

# Create the list of Team objects
teams = [
    Team("percentage_r0ckman", 21, 0, 12499, 9286),
    Team("percentage_LactosePapi", 16, 5, 11001, 9603),
    Team("percentage_tjwalter", 14, 7, 10328, 9181),
    Team("percentage_mbarbone99", 13, 8, 10850, 10096),
    Team("percentage_Beaverr", 13, 8, 10754, 9856),
    Team("percentage_BuyFSR", 11, 10, 10182, 10063),
    Team("percentage_jjgambino9", 9, 12, 9976, 10399),
    Team("percentage_MrPuffy", 9, 12, 9485, 9684),
    Team("percentage_Fashion", 9, 12, 9466, 10521),
    Team("percentage_mikeyRC", 5, 16, 8129, 10288),
    Team("percentage_youwearmetobed", 4, 17, 8486, 10614),
    Team("percentage_Nimeshh", 2, 19, 8681, 10246)
]

# Instantiate FantasyBasketballManager
manager = FantasyBasketballManager()

# Sort the teams
manager.sort_teams(teams)

# Display the sorted teams
for idx, team in enumerate(teams, 1):
    print(f"{idx}. {team.name} - Wins: {team.wins}, Losses: {team.losses}, Points For: {team.points_for}, Points Against: {team.points_against}")
