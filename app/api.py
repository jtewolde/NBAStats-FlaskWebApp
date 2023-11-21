"""
NBA Stats Web App
Developed by: Joseph Tewolde
Description: This is a web app that will display NBA stats for the 2023-2024 season.

"""

from nba_api.stats.static import teams, players
from nba_api import stats
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, playergamelog
from pandas import DataFrame
# from models import User, Team, Player, PlayerStatsPerGame
# from app import db


def get_teams():
    """ This function will return a list of the names of all NBA teams."""
    nba_teams = teams.get_teams()

    return nba_teams

    # for team in nba_teams:
    #     team_object = Team(
    #         team_name=team['full_name'],
    #         team_abbreviation=team['abbreviation'],
    #         team_city=team['city'],
    #         team_state=team['state'],
    #         year_founded=team['year_founded']
    #     )
    #     db.session.add(team_object)
    #     team_objects.append(team_object)

    # db.session.commit()
    
    # return team_objects

def get_players():
    """ This function will return a list of all NBA players in the 2023-2024 season."""
    nba_players = players.get_active_players()

    return nba_players

    # for player in nba_players:
    #     player_object = Player(
    #         player_name=player['full_name'],
    #         player_id=player['id']
    #     )
    #     db.session.add(player_object)
    #     player_objects.append(player_object)

    # db.session.commit()
    
    # return player_objects


def get_player_total_stats(player_name):
    """ This function will return a dictionary of the stats per game of a given player."""
    player = [player for player in players.get_active_players() if player['full_name'] == player_name][0] # Get the player
    player_id = player['id']
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]
    stats_df = career_df[career_df['SEASON_ID'] == '2023-24']
    stats_df = stats_df[['PTS', 'AST', 'REB', 'STL', 'BLK', 'GP', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'TOV']]
    stats_dict = stats_df.to_dict('records')[0]
    return stats_dict

def get_player_avg_stats(player_name):
    """ This function will return a dictionary of the stats per game of a given player."""
    active_players = players.get_active_players()

    matching_players = [player for player in active_players if player['full_name'] == player_name] # Get the player

    if not matching_players: # If the player does not exist
        print("This player does not exist!")
        return None

    player = matching_players[0]# Get the player ID
    player_id = player['id'] # Get the player ID

    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]
    stats_df = career_df[career_df['SEASON_ID'] == '2023-24'] # Get the stats for the 2023-24 season

    stats_df = stats_df[['PTS', 'AST', 'REB', 'STL', 'BLK', 'GP', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'TOV']]
    
    # Calculate per game averages
    stats_df['PTS'] /= stats_df['GP']
    stats_df['AST'] /= stats_df['GP']
    stats_df['REB'] /= stats_df['GP']
    stats_df['STL'] /= stats_df['GP']
    stats_df['BLK'] /= stats_df['GP']
    stats_df['FG%'] = stats_df['FGM'] / stats_df['FGA'] * 100
    stats_df['FG3%'] = stats_df['FG3M'] / stats_df['FG3A'] * 100
    stats_df['FT%'] = stats_df['FTM'] / stats_df['FTA'] * 100
    stats_df['TOV'] /= stats_df['GP']
    
    
    # Drop the 'GP' column as it's no longer needed
    stats_df = stats_df[['PTS', 'AST', 'REB', 'STL', 'BLK', 'FG%', 'FG3%', 'FT%', 'TOV', 'GP']]
    stats_df = stats_df.round(1) # Round all values to 2 decimal places
    
    # Convert the per game averages to a dictionary
    stats_dict = stats_df.to_dict('records')[0]

    # print(player_name) # Print the player name
    return stats_dict # Return the dictionary
    

def get_player_avg_stats_career(player_name):
    """ This function will return a dictionary of the stats per game for each season of a given player's career."""
    active_players = players.get_active_players()

    matching_players = [player for player in active_players if player['full_name'] == player_name] # Get the player

    if not matching_players: # If the player does not exist
        print("This player does not exist!")
        return None

    player = matching_players[0]# Get the player ID
    player_id = player['id'] # Get the player ID

    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]

    # Extract relevant columns
    stats_df = career_df[['SEASON_ID', 'PTS', 'AST', 'REB', 'STL', 'BLK', 'GP', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'TOV']]

    # Calculate per game averages
    stats_df.loc[:, 'PTS'] /= stats_df['GP']
    stats_df.loc[:, 'AST'] /= stats_df['GP']
    stats_df.loc[:, 'REB'] /= stats_df['GP']
    stats_df.loc[:, 'STL'] /= stats_df['GP']
    stats_df.loc[:, 'BLK'] /= stats_df['GP']
    stats_df.loc[:, 'FG%'] = stats_df['FGM'] / stats_df['FGA'] * 100
    stats_df.loc[:, 'FG3%'] = stats_df['FG3M'] / stats_df['FG3A'] * 100
    stats_df.loc[:, 'FT%'] = stats_df['FTM'] / stats_df['FTA'] * 100
    stats_df.loc[:, 'TOV'] /= stats_df['GP']
    
    # Drop the 'GP' column as it's no longer needed
    stats_df = stats_df[['SEASON_ID', 'PTS', 'AST', 'REB', 'STL', 'BLK', 'FG%', 'FG3%', 'FT%', 'TOV', 'GP']]
    stats_df = stats_df.round(1) # Round all values to 1 decimal place

    # Convert the per game averages to a list of dictionaries
    stats_list = stats_df.to_dict('records')

    return stats_list # Return the list of dictionaries


def get_team_roster(team_name):
    """ This function will return a list of all players for a given team."""
    nba_players = get_players()  # Get all NBA players
    nba_teams = get_teams()  # Get all NBA teams
    team = next((t for t in nba_teams if t['full_name'] == team_name), None)  # Get the team that matches the team name

    team_roster = []  # Initialize an empty list for the team roster

    if team:  # If the team exists
        player_team_abbreviation = team['abbreviation'] # Get the team abbreviation

        for player in nba_players:  # For each player
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player['id']) # Get the player info
            player_info_df = player_info.get_data_frames()[0] # Convert the player info to a dataframe
            player_team = player_info_df['TEAM_ABBREVIATION'].iloc[0] # Get the player's team abbreviation

            if player_team == player_team_abbreviation: # If the player's team abbreviation matches the team abbreviation
                print("Player added to team roster: ")
                print(player_info_df['DISPLAY_FIRST_LAST'].iloc[0]) # Print the player's name
                team_roster.append(player_info_df['DISPLAY_FIRST_LAST'].iloc[0])  # Add the player to the team roster

    return team_roster # Return the team roster

   
def get_gamelog(player_name):
    """ This function will return a dataframe of the gamelog for a given player."""
    active_players = players.get_active_players()
    print(player_name)

    matching_players = [player for player in active_players if player['full_name'] == player_name] # Get the player

    if not matching_players: # If the player does not exist
        print("This player does not exist!")
        return None

    player = matching_players[0]# Get the player ID
    player_id = player['id'] # Get the player ID

    gamelog = playergamelog.PlayerGameLog(player_id=player_id)
    gamelog_df = gamelog.get_data_frames()[0]

    gamelog_df['FG_PCT'] = gamelog_df['FG_PCT'] * 100 # Convert the FG% to a percentage
    gamelog_df['FG3_PCT'] = gamelog_df['FG3_PCT'] * 100 # Convert the FG3% to a percentage
    gamelog_df['FT_PCT'] = gamelog_df['FT_PCT'] * 100 # Convert the FT% to a percentage

    gamelog_df['FG_PCT'] = gamelog_df['FG_PCT'].round(1) # Round the FG% to 1 decimal place
    gamelog_df['FG3_PCT'] = gamelog_df['FG3_PCT'].round(1) # Round the FG3% to 1 decimal place
    gamelog_df['FT_PCT'] = gamelog_df['FT_PCT'].round(1) # Round the FT% to 1 decimal place

    gamelog_list = gamelog_df[['GAME_DATE', 'MATCHUP', 'WL', 'PTS', 'AST', 'REB', 'OREB','DREB', 'STL', 'BLK', 'FG_PCT', 'FGM', 'FGA', 'FG3_PCT', 'FG3M', 'FG3A', 'FT_PCT', 'FTM', 'FTA', 'TOV', 'PF', 'PLUS_MINUS', 'MIN']] # Extract relevant columns
    gamelog_list = gamelog_list.to_dict('records') # Convert the dataframe to a list of dictionaries

    return gamelog_list # Return the list of dictionaries

if __name__ == "__main__":
    # print(get_team_roster('Portland Trail Blazers'))

    # print(get_player_total_stats('Nikola Jokic'))
    # print(get_player_total_stats('LeBron James'))  # These lines will return the total stats for the 2023-24 season
    # print(get_player_total_stats('Stephen Curry'))

    # print(get_player_avg_stats('Stephen Curry'))
    # print(get_player_avg_stats('Nikola Jokic'))  # These lines will return the per game averages for the 2023-24 season
    # print(get_player_avg_stats('LeBron James'))
    # print(get_player_avg_stats('Kevin Durant'))

    print(get_player_avg_stats_career('Stephen Curry'))
    