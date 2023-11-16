"""
NBA Stats Web App
Developed by: Joseph Tewolde
Description: This is a web app that will display NBA stats for the 2023-2024 season.

"""

from nba_api.stats.static import teams, players
from nba_api import stats
from nba_api.stats.endpoints import playercareerstats
from pandas import DataFrame


def get_teams():
    """ This function will return a list of the names of all NBA teams."""
    nba_teams = teams.get_teams()
    team_names = [team['full_name'] for team in nba_teams]
    return team_names

def get_players():
    """ This function will return a list of all NBA players in the 2023-2024 season."""
    nba_players = players.get_active_players()
    player_names = [player['full_name'] for player in nba_players]
    return player_names

def get_player_total_stats(player_name):
    """ This function will return a dictionary of the stats per game of a given player."""
    player = [player for player in players.get_active_players() if player['full_name'] == player_name][0]
    player_id = player['id']
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]
    stats_df = career_df[career_df['SEASON_ID'] == '2023-24']
    stats_df = stats_df[['PTS', 'AST', 'REB', 'STL', 'BLK']]
    stats_dict = stats_df.to_dict('records')[0]
    return stats_dict

def get_player_avg_stats(player_name):
    """ This function will return a dictionary of the stats per game of a given player."""
    player = [player for player in players.get_active_players() if player['full_name'] == player_name][0]
    player_id = player['id']
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]
    stats_df = career_df[career_df['SEASON_ID'] == '2023-24']
    stats_df = stats_df[['PTS', 'AST', 'REB', 'STL', 'BLK', 'GP', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA']]
    
    # Calculate per game averages
    stats_df['PTS'] /= stats_df['GP']
    stats_df['AST'] /= stats_df['GP']
    stats_df['REB'] /= stats_df['GP']
    stats_df['STL'] /= stats_df['GP']
    stats_df['BLK'] /= stats_df['GP']
    stats_df['FG%'] = stats_df['FGM'] / stats_df['FGA'] * 100
    stats_df['FG3%'] = stats_df['FG3M'] / stats_df['FG3A'] * 100
    stats_df['FT%'] = stats_df['FTM'] / stats_df['FTA'] * 100

    
    # Drop the 'GP' column as it's no longer needed
    stats_df = stats_df[['PTS', 'AST', 'REB', 'STL', 'BLK', 'FG%', 'FG3%', 'FT%']]
    
    # Convert the per game averages to a dictionary
    stats_dict = stats_df.to_dict('records')[0]
    
    return stats_dict



if __name__ == "__main__":
    print(get_teams())
    # print(get_players())
    print(get_player_total_stats('Nikola Jokic'))
    print(get_player_avg_stats('Nikola Jokic'))
    print(get_player_total_stats('LeBron James'))
    print(get_player_avg_stats('LeBron James'))
    print(get_player_total_stats('Stephen Curry'))
    print(get_player_avg_stats('Stephen Curry'))