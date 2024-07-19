"""
NBA Stats Web App
Developed by: Joseph Tewolde
Description: This is a web app that will display NBA stats for the 2023-2024 season.

"""

from nba_api.stats.static import teams, players
from nba_api import stats
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, playergamelog, commonteamroster, leaguestandings, teamgamelog, scoreboard
from pandas import DataFrame
# from models import User, Team, Player, PlayerStatsPerGame
# from app import db


def get_teams():
    """ This function will return a list of the names of all NBA teams."""
    nba_teams = teams.get_teams()

    return nba_teams


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
    stats_df = career_df[['SEASON_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'PTS', 'AST', 'REB', 'STL', 'BLK', 'GP', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'TOV']]

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
    stats_df = stats_df[['SEASON_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'PTS', 'AST', 'REB', 'STL', 'BLK', 'FG%', 'FG3%', 'FT%', 'TOV', 'GP']]
    stats_df = stats_df.round(1) # Round all values to 1 decimal place

    # Convert the per game averages to a list of dictionaries
    stats_list = stats_df.to_dict('records')

    return stats_list # Return the list of dictionaries


def get_team_roster(team_name):
    """ This function will return a list of all players for a given team."""
    nba_teams = teams.get_teams()
    matching_teams = [team for team in nba_teams if team['full_name'] == team_name] # Get the team

    if not matching_teams: # If the team does not exist
        print("This team does not exist!")
        return None

    team = matching_teams[0] # Get the team ID
    team_id = team['id'] # Get the team ID

    roster = commonteamroster.CommonTeamRoster(team_id=team_id)
    roster_df = roster.get_data_frames()[0]
    roster_list = roster_df[['PLAYER', 'NUM', 'POSITION', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE', 'AGE', 'EXP', 'SCHOOL']].to_dict('records') # Extract relevant columns

    return roster_list # Return the list of dictionaries

   
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

def get_league_standings():
    """ This function will return a dataframe of the league standings."""
    standings = leaguestandings.LeagueStandings() # Get the league standings
    standings_df = standings.get_data_frames()[0] # Convert the standings to a dataframe

    standings_df = standings_df[['TeamID', 'TeamCity', 'TeamName', 'Conference', 'ConferenceRecord', 'Division', 'DivisionRecord', 'PlayoffRank', 'Record', 'WinPCT', 'HOME', 'ROAD', 'L10', 'CurrentStreak']] # Extract relevant columns

    # standings_df['ConferenceRecord'] = standings_df['ConferenceRecord'].str.replace('-', ' - ') # Replace the '-' with ' - ' in the ConferenceRecord column
    # standings_df['DivisionRecord'] = standings_df['DivisionRecord'].str.replace('-', ' - ') # Replace the '-' with ' - ' in the DivisionRecord column
    # standings_df['L10'] = standings_df['L10'].str.replace('-', ' - ') # Replace the '-' with ' - ' in the L10 column


    standings_df = standings_df.round(3) # Round all values to 3 decimal places

    standings_list = standings_df.to_dict('records') # Convert the dataframe to a list of dictionaries

    return standings_list # Return the list of dictionaries

def get_western_standings():
    """ This function will return a dataframe of the western conference standings."""
    standings = leaguestandings.LeagueStandings() # Get the league standings
    standings_df = standings.get_data_frames()[0] # Convert the standings to a dataframe

    standings_df = standings_df[['TeamID', 'TeamCity', 'TeamName', 'Conference', 'ConferenceRecord', 'Division', 'DivisionRecord', 'PlayoffRank', 'Record', 'WinPCT', 'HOME', 'ROAD', 'L10', 'CurrentStreak']] # Extract relevant columns

    standings_df = standings_df[standings_df['Conference'] == 'West'] # Get only the western conference standings

    # standings_df['ConferenceRecord'] = standings_df['ConferenceRecord'].str.replace('-', ' - ') # Replace the '-' with ' - ' in the ConferenceRecord column
    # standings_df['DivisionRecord'] = standings_df['DivisionRecord'].str.replace('-', ' - ') # Replace the '-' with ' - ' in the DivisionRecord column
    # standings_df['L10'] = standings_df['L10'].str.replace('-', ' - ') # Replace the '-' with ' - ' in the L10 column


    standings_df = standings_df.round(3) # Round all values to 3 decimal places

    standings_list = standings_df.to_dict('records') # Convert the dataframe to a list of dictionaries

    return standings_list # Return the list of dictionaries

def get_eastern_standings():
    """ This function will return a dataframe of the eastern conference standings."""
    standings = leaguestandings.LeagueStandings() # Get the league standings
    standings_df = standings.get_data_frames()[0] # Convert the standings to a dataframe

    standings_df = standings_df[['TeamID', 'TeamCity', 'TeamName', 'Conference', 'ConferenceRecord', 'Division', 'DivisionRecord', 'PlayoffRank', 'Record', 'WinPCT', 'HOME', 'ROAD', 'L10', 'CurrentStreak']] # Extract relevant columns

    standings_df = standings_df[standings_df['Conference'] == 'East'] # Get only the eastern conference standings

    # standings_df['ConferenceRecord'] = standings_df['ConferenceRecord'].str.replace('-', ' - ') # Replace the '-' with ' - ' in the ConferenceRecord column
    # standings_df['DivisionRecord'] = standings_df['DivisionRecord'].str.replace('-', ' - ') # Replace the '-' with ' - ' in the DivisionRecord column
    # standings_df['L10'] = standings_df['L10'].str.replace('-', ' - ') # Replace the '-' with ' - ' in the L10 column


    standings_df = standings_df.round(3) # Round all values to 3 decimal places

    standings_list = standings_df.to_dict('records') # Convert the dataframe to a list of dictionaries

    return standings_list # Return the list of dictionaries

def get_team_gamelog(team_name):
    """ This function will return a dataframe of the gamelog for a given team."""
    nba_teams = teams.get_teams()
    matching_teams = [team for team in nba_teams if team['full_name'] == team_name] # Get the team

    if not matching_teams: # If the team does not exist
        print("This team does not exist!")
        return None

    team = matching_teams[0] # Get the team ID
    team_id = team['id'] # Get the team ID

    gamelog = teamgamelog.TeamGameLog(team_id=team_id)
    gamelog_df = gamelog.get_data_frames()[0]

    gamelog_df['FG_PCT'] = gamelog_df['FG_PCT'] * 100 # Convert the FG% to a percentage
    gamelog_df['FG3_PCT'] = gamelog_df['FG3_PCT'] * 100 # Convert the FG3% to a percentage
    gamelog_df['FT_PCT'] = gamelog_df['FT_PCT'] * 100 # Convert the FT% to a percentage

    gamelog_df['FG_PCT'] = gamelog_df['FG_PCT'].round(1) # Round the FG% to 1 decimal place
    gamelog_df['FG3_PCT'] = gamelog_df['FG3_PCT'].round(1) # Round the FG3% to 1 decimal place
    gamelog_df['FT_PCT'] = gamelog_df['FT_PCT'].round(1) # Round the FT% to 1 decimal place

    gamelog_list = gamelog_df[['Game_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'PTS', 'AST', 'REB', 'OREB','DREB', 'STL', 'BLK', 'FG_PCT', 'FGM', 'FGA', 'FG3_PCT', 'FG3M', 'FG3A', 'FT_PCT', 'FTM', 'FTA', 'TOV', 'PF',  'MIN']] # Extract relevant columns
    gamelog_list = gamelog_list.to_dict('records') # Convert the dataframe to a list of dictionaries

    return gamelog_list # Return the list of dictionaries

def get_team_name(team_id):
    """ This function will return the name of a team given its ID."""
    nba_teams = teams.get_teams()
    matching_teams = [team for team in nba_teams if team['id'] == team_id] # Get the team

    if not matching_teams: # If the team does not exist
        print("This team does not exist!")
        return None

    team = matching_teams[0] # Get the team name
    team_name = team['full_name'] # Get the team name

    return team_name # Return the team name

def get_todays_games():
    """ This function will return a dataframe of today's games."""
    todays_games = scoreboard.Scoreboard().game_header # Get today's games
    todays_games_df = todays_games.get_data_frame() # Convert today's games to a dataframe


    todays_games_list = todays_games_df[['GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 'GAME_STATUS_ID', 'GAME_STATUS_TEXT', 'GAMECODE', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'SEASON', 'LIVE_PERIOD', 'LIVE_PC_TIME', 'NATL_TV_BROADCASTER_ABBREVIATION', 'LIVE_PERIOD_TIME_BCAST', 'WH_STATUS']]
    todays_games_list = todays_games_list.to_dict('records') # Convert the dataframe to a list of dictionaries

    return todays_games_list # Return the list of dictionaries

def get_playoff_statistics_career(player_name):
    """ This function will return a dictionary of the playoff statistics for each season of a given player's career."""
    active_players = players.get_active_players()

    matching_players = [player for player in active_players if player['full_name'] == player_name] # Get the player

    if not matching_players: # If the player does not exist
        print("This player does not exist!")
        return None

    player = matching_players[0]# Get the player ID
    player_id = player['id'] # Get the player ID

    career = playercareerstats.PlayerCareerStats(player_id=player_id).season_totals_post_season # Get the playoff statistics
    career_df = career.get_data_frame()
    # Extract relevant columns
    stats_df = career_df[['SEASON_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE','PTS', 'AST', 'REB', 'STL', 'BLK', 'GP', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'TOV']]

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
    stats_df = stats_df[['SEASON_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE','PTS', 'AST', 'REB', 'STL', 'BLK', 'FG%', 'FG3%', 'FT%', 'TOV', 'GP']]
    stats_df = stats_df.round(1) # Round all values to 1 decimal place

    # Convert the per game averages to a list of dictionaries
    stats_list = stats_df.to_dict('records')

    return stats_list #


if __name__ == "__main__":


    print(get_playoff_statistics_career('Stephen Curry')) # This line will return the playoff statistics for a given player

    