from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email_address = db.Column(db.String)
    about = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String)
    team_abbreviation = db.Column(db.String)
    team_city = db.Column(db.String)
    team_state = db.Column(db.String)
    year_founded = db.Column(db.Integer)


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    player_name = db.Column(db.String)


class PlayerStatsPerGame(db.Model):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player_name = db.Column(db.String)
    player_points = db.Column(db.Float)
    player_assists = db.Column(db.Float)
    player_rebounds = db.Column(db.Float)
    player_steals = db.Column(db.Float)
    player_blocks = db.Column(db.Float)
    player_fg_percent = db.Column(db.Float)
    player_fg3_percent = db.Column(db.Float)
    player_ft_percent = db.Column(db.Float)
    player_turnovers = db.Column(db.Float)
    player_games_played = db.Column(db.Integer)

    player = db.relationship('Player', backref='player_stats') # create a relationship between the player and the player stats

class PlayerStatsTotal(db.Model):
    __tablename__ = 'player_stats_total'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player_name = db.Column(db.String)
    player_points = db.Column(db.Integer)
    player_assists = db.Column(db.Integer)
    player_rebounds = db.Column(db.Integer)
    player_steals = db.Column(db.Integer)
    player_blocks = db.Column(db.Integer)
    player_fg_attempts = db.Column(db.Integer)
    player_fg_made = db.Column(db.Integer)
    player_fg3_attempts = db.Column(db.Integer)
    player_fg3_made = db.Column(db.Integer)
    player_ft_attempts = db.Column(db.Integer)
    player_ft_made = db.Column(db.Integer)
    player_turnovers = db.Column(db.Integer)
    player_games_played = db.Column(db.Integer)

    player = db.relationship('Player', backref='player_stats_total') # create a relationship between the player and the player stats


