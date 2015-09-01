#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    c = connect()
    cursor = c.cursor()
    cursor.execute('delete from score;')
    cursor.execute('delete from match;')
    c.commit()
    c.close()

def deletePlayers():
    """Remove all the player records from the database."""
    c = connect()
    cursor = c.cursor()
    cursor.execute('delete from player;')
    c.commit()
    c.close()

def countPlayers():
    """Returns the number of players currently registered."""
    c = connect()
    cursor = c.cursor()
    cursor.execute('select count(*) from player;')
    rows = cursor.fetchall()
    c.close()
    return int(rows[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    c = connect()
    cursor = c.cursor()
    cursor.execute('insert into player (name) values (%s)', (name,))
    c.commit()
    c.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    c = connect()
    cursor = c.cursor()
    cursor.execute('select player.id, name, wins, matches from player, winstat, matchstat where player.id=winstat.id and player.id=matchstat.id order by wins desc,matches;')
    rows = cursor.fetchall()
    
    c.close()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c = connect()
    cursor = c.cursor()
    cursor.execute('insert into match (name) values (%s) returning id', (str(winner)+str(loser),))
    c.commit()
    rows = cursor.fetchall()
    cursor.execute('insert into score (matchid, playerid, score) values (%s, %s, %s)', (rows[0][0],str(winner),'1'))
    cursor.execute('insert into score (matchid, playerid, score) values (%s, %s, %s)', (rows[0][0],str(loser),'-1'))
    c.commit()
    c.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    orders = playerStandings()
    li = []
    total = []
    count = False
    for item in orders:
        li.append(item[0])
        li.append(item[1])
        if count:
            total.append(tuple(li))
            li = []
        count = not count
    return tuple(total)
