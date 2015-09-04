rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses

The tournament folder contains a relational database for swiss pairing.

Running environment:
postGreSQL,
python.

Steps:
1. open postgresql (type "psql")
2. create a database called "tournament" (create database tournament;)
3. connect to the database (\c tournament)
4. run the sql commands in file "tournament.sql"
5. exit database(\q)
6. run a test (python tournament_test.py)
7. Funcitons are introduced in the following:

File "tournament.sql" contains several commands for creating the tables in database "tournament". The commands in this file should be implemented before running the functions in "tournament.py".
These tables include:
player: player info,
match: match info including ids of winner and loser,
winstat: players' ids and # of wins,
matchstat: player' ids and # of matches.

File "tournament.py" contains several functions for operating the database.
deleteMatches(): remove all the matches,
deletePlayers(): remove all the players,
countPlayers(): count the number of players,
registerPlayer(name): add a player by name,
playerStandings(): rank the players according to the win records. returning a list of tuples. Each tuple contains (id, name, wins, matches),
reportMatch(winner, loser): report a match.
swissPairings(): pair up players according to their numbers of wins.

running the file "tournament_test.py" can test the feasibility of functions in "tournament.py".


