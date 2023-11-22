from app import app, db, load_user
from app.models import User, Team, Player, PlayerStatsPerGame, PlayerStatsTotal
from app.forms import SignUpForm, SignInForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt, uuid
from api import get_teams, get_team_roster, get_players, get_player_avg_stats, get_player_total_stats, get_gamelog, get_player_avg_stats_career, get_league_standings
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    """ This route handles the signin process, authenticating the user and redirecting the user to the orders page. """
    form = SignInForm() # instantiate a signin form
    if form.validate_on_submit(): 
        user = User.query.filter_by(id=form.id.data).first() # check if the user exists using the id
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd): # if the user exists and the password matches
            login_user(user) # login the user
            return redirect(url_for('teams')) # redirect the user to the orders page
        else:
            return '<p>Sorry, the user id and/or password are incorrect!</p>' # print an error message
    return render_template('signin.html', form=form) # render the signin template if the form was not submitted or it is not valid

@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    """ This route handles the signup process, creating a new user and storing it in the local database,
        and then redirecting the user to the signin page, and create a Square customer for the user. """
    form = SignUpForm() # instantiate a signup form
    if form.validate_on_submit(): # if the form was submitted and it is valid
        existing_user = User.query.filter_by(id=form.id.data).first() # check if the user already exists using the id
        if existing_user: # if the user already exists
            return '<p>Sorry, this user id is already taken!</p>' # print an error message

        passwd = form.passwd.data # get the password from the form
        passwd_confirm = form.passwd_confirm.data # get the password confirmation from the form

        if passwd == passwd_confirm: # if the password and the password confirmation match
            salt_passwd = bcrypt.gensalt() # generate a salt
            hashed_passwd = bcrypt.hashpw(passwd.encode('utf-8'), salt_passwd) # hash the password using the salt

            # create a new user 
            new_user = User(id=form.id.data, email_address = form.email_address.data, about = form.about.data, passwd=hashed_passwd) # instantiate a new user with the id, customer_id, and hashed password
            db.session.add(new_user) # add the new user to the database
            db.session.commit() # commit the changese

            return redirect(url_for('users_signin')) # redirect the user to the signin page
        else: # if the password and the password confirmation do not match
            return '<p>Sorry, the password and the password confirmation do not match!</p>'
    return render_template('signup.html', form=form) # render the signup template if the form was not submitted or it is not valid

    
@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    """This route handles the signout process, logging out the user and redirecting the user to the index page."""
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/players', methods=['GET', 'POST'])
def show_players():
    """This route handles the players page, displaying all NBA players."""
    for player in get_players():
        player_object = Player(
            player_name=player['full_name'],
            player_id=player['id']
        )
        if db.session.query(Player).filter_by(player_id=player['id']).count() == 0: # if the player does not exist in the database
            db.session.add(player_object) # add the new player to the database
            db.session.commit() # commit the changes
    return render_template('players.html', players=get_players()) # render the players template
    
@login_required
@app.route('/teams', methods=['GET', 'POST'])
def teams():
    """This route handles the teams page, displaying all NBA teams."""
    for team in get_teams():
        team_object = Team(
            team_name=team['full_name'],
            team_abbreviation=team['abbreviation'],
            team_city=team['city'],
            team_state=team['state'],
            year_founded=team['year_founded']
        )
        db.session.add(team_object) # add the new team to the database

    if db.session.query(Team).count() == 0: # if the database is empty
        print('Database is empty!')
        db.session.commit() # commit the changes

    return render_template('teams.html', teams=get_teams()) # render the teams template

@login_required
@app.route('/players/stats', methods=['GET', 'POST'])
def show_players_per_game_stats():
    """ This route handles the player stats page, displaying all NBA players stats per game."""
    player_name = request.args.get('player') # get the player name from the request
    player_id = [player for player in players.get_active_players() if player['full_name'] == player_name][0]['id'] # get the player id from the player name

    print(player_name)

    player_stats = get_player_avg_stats(player_name) # get the player stats

    player_avg_stats = PlayerStatsPerGame( # instantiate a new player stats object
        player_id=player_id,
        player_name=player_name,
        player_points=player_stats['PTS'],
        player_assists=player_stats['AST'], 
        player_rebounds=player_stats['REB'], 
        player_steals=player_stats['STL'],
        player_blocks=player_stats['BLK'],
        player_fg_percent=player_stats['FG%'],
        player_fg3_percent=player_stats['FG3%'],
        player_ft_percent=player_stats['FT%'],
        player_turnovers=player_stats['TOV'],
        player_games_played=player_stats['GP']
    )

    print(player_avg_stats)
    print(player_stats)

    if db.session.query(PlayerStatsPerGame).filter_by(player_name=player_name).count() == 0: # if the player does not exist in the database
        db.session.add(player_avg_stats) # add the new player to the database
        db.session.commit() # commit the changes
    return render_template('avg_stats.html', player_stats=player_stats, player_name=player_name) # render the player stats template


@login_required
@app.route('/players/stats/total', methods=['GET', 'POST'])
def show_players_total_stats():
    """ This route handles the player stats page, displaying all NBA players stats per game."""
    player_name = request.args.get('player') # get the player name from the request
    player_id = [player for player in players.get_active_players() if player['full_name'] == player_name][0]['id']
    print(player_name)

    player_stats = get_player_total_stats(player_name) # get the player stats

    player_total_stats = PlayerStatsTotal( # instantiate a new player stats object
        player_id=player_id,
        player_name=player_name,
        player_points=player_stats['PTS'],
        player_assists=player_stats['AST'], 
        player_rebounds=player_stats['REB'], 
        player_steals=player_stats['STL'],
        player_blocks=player_stats['BLK'],
        player_fg_attempts=player_stats['FGA'],
        player_fg_made=player_stats['FGM'],
        player_fg3_attempts=player_stats['FG3A'],
        player_fg3_made=player_stats['FG3M'],
        player_ft_attempts=player_stats['FTA'],
        player_ft_made=player_stats['FTM'],
        player_turnovers=player_stats['TOV'],
        player_games_played=player_stats['GP']
    )

    print(player_total_stats)
    print(player_stats)

    if db.session.query(PlayerStatsTotal).filter_by(player_name=player_name).count() == 0: # if the player does not exist in the database
        db.session.add(player_total_stats)
        db.session.commit()
    return render_template('total_stats.html', player_stats=player_stats, player_name=player_name) # render the player stats template

@login_required
@app.route('/roster', methods=['GET', 'POST'])
def teams_roster():
    """ This route handles the roster page, displaying all players in a given team. """
    team = request.args.get('team') # get the team name from the request
  
    print(team) # print the team name

    roster = get_team_roster(team) # get the team roster
    return render_template('roster.html', roster=roster, team_name=team)

@login_required
@app.route('/players/gamelog', methods=['GET', 'POST'])
def show_players_gamelog():
    """ This route handles the gamelog page, displaying the gamelog of a given player. """
    player_name = request.args.get('player') # get the player name from the request
   
    player_gamelog = get_gamelog(player_name) # get the player gamelog
    return render_template('game_log.html', gamelog=player_gamelog, player_name=player_name)

@login_required
@app.route('/players/career', methods=['GET', 'POST'])
def show_players_career():
    """ This route handles the career page, displaying the career stats of a given player. """
    player_name = request.args.get('player') # get the player name from the request

    player_career_stats = get_player_avg_stats_career(player_name) # get the player career stats
    return render_template('career_stats.html', career_stats=player_career_stats, player_name=player_name)

@login_required
@app.route('/league/standings', methods=['GET', 'POST'])
def show_league_standings():
    """ This route handles the standings page, displaying the league standings. """

    league_standings = get_league_standings()
    return render_template('league_standings.html', standings=league_standings)

