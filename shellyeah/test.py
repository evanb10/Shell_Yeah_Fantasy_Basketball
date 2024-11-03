def average_odds(teams):
    # Step 1: Group teams by (wins, losses)
    team_groups = {}
    for team in teams:
        key = (team['wins'], team['losses'])
        if key not in team_groups:
            team_groups[key] = []
        team_groups[key].append(team)

    # Step 2: Calculate average odds for each group with more than one team
    results = []
    for (wins, losses), grouped_teams in team_groups.items():
        if len(grouped_teams) > 1:
            # Calculate average odds
            avg_odds = sum(team['odds'] for team in grouped_teams) / len(grouped_teams)
            for team in grouped_teams:
                team['odds'] = avg_odds  # Update each team in the group with the average odds
        results.extend(grouped_teams)

    return results

# Test data
teams_data = [
    {"team": "Nimeshh", "rank": 12, "wins": 2, "losses": 19, "odds": 30, "points_for": 8681, "points_against": 10246},
    {"team": "youwearmetobed", "rank": 11, "wins": 4, "losses": 17, "odds": 25, "points_for": 8486, "points_against": 10614},
    {"team": "mikeyRC", "rank": 10, "wins": 5, "losses": 16, "odds": 20, "points_for": 8129, "points_against": 10288},
    {"team": "jjgambino9", "rank": 9, "wins": 9, "losses": 12, "odds": 15, "points_for": 9466, "points_against": 10521},
    {"team": "MrPuffy", "rank": 8, "wins": 9, "losses": 12, "odds": 10, "points_for": 9485, "points_against": 9684},
    {"team": "Fashion", "rank": 7, "wins": 9, "losses": 12, "odds": 0, "points_for": 9976, "points_against": 10399},
    {"team": "BuyFSR", "rank": 6, "wins": 11, "losses": 10, "odds": 0, "points_for": 10182, "points_against": 10063},
    {"team": "mbarbone99", "rank": 5, "wins": 13, "losses": 8, "odds": 0, "points_for": 10754, "points_against": 9856},
    {"team": "Beaverr", "rank": 4, "wins": 13, "losses": 8, "odds": 0, "points_for": 10850, "points_against": 10096},
    {"team": "tjwalter", "rank": 3, "wins": 14, "losses": 7, "odds": 0, "points_for": 10328, "points_against": 9181},
    {"team": "LactosePapi", "rank": 2, "wins": 16, "losses": 5, "odds": 0, "points_for": 11001, "points_against": 9603},
    {"team": "r0ckman", "rank": 1, "wins": 21, "losses": 0, "odds": 0, "points_for": 12499, "points_against": 9286},
]

# Calculate and display updated odds
updated_teams = average_odds(teams_data)
for team in updated_teams:
    print(f"Team: {team['team']}, Wins: {team['wins']}, Losses: {team['losses']}, Odds: {team['odds']}")

