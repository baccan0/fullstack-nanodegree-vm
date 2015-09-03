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
    # Delete all the columns in match.
    cursor.execute('delete from match;')
    c.commit()
    c.close()

def deletePlayers():
    """Remove all the player records from the database."""
    c = connect()
    cursor = c.cursor()
    # Delete all the columns in player.
    cursor.execute('delete from player;')
    c.commit()
    c.close()

def countPlayers():
    """Returns the number of players currently registered."""
    c = connect()
    cursor = c.cursor()
    # Count columns in player.
    cursor.execute('select count(*) from player;')
    rows = cursor.fetchall()
    c.close()
    # Return the first entry which is the count.
    return rows[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    c = connect()
    cursor = c.cursor()
    # Insert a player's name, id is generated automatically.
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
    # Combine player table with views of winstat and matchstat.
    # Sort the player according to # of wins and # of matches. Players having more wins and less matches have higher ranks. 
    cursor.execute('select player.id, name, wins, matches from player, winstat, matchstat where player.id=winstat.id and player.id=matchstat.id order by wins desc,matches;')
    rows = cursor.fetchall()
    
    c.close()
    # Return the list of player standings called rows.
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c = connect()
    cursor = c.cursor()
    # Insert the match with winner and loser.
    cursor.execute('insert into match (winner, loser) values (%s,%s) returning id', (winner,loser))
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
    # Get the ranks.
    orders = playerStandings()
    # List to contain player pair temporarily.
    li = []
    # List to contain all the tuples of player pairs.
    total = []
    # A boolean variable to distinguish odd or even order of player standing.
    count = False
    for item in orders:
        # Player id and name are appended to temporary container.
        li.append(item[0])
        li.append(item[1])
        if count:
            # Pair is appended to the final container and then empty the temporary container.
            total.append(tuple(li))
            li = []
        count = not count
    # Return the list of all the tuples of player pairs.
    return total
