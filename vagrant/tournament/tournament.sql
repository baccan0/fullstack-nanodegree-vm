-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Table for players' info (id, name).
CREATE TABLE player (id   serial      PRIMARY KEY, 
                     name varchar(40) NOT NULL);

-- Table for matches, winners and losers.
CREATE TABLE match(id     serial  PRIMARY KEY, 
                   winner integer REFERENCES player(id), 
                   loser  integer REFERENCES player(id));

-- View for win stats on each player (id, # of wins).
CREATE VIEW winstat as 
select player.id,
       count(winner) as wins 
from player 
left join match 
on player.id = winner 
group by player.id;

-- View for match stats on each player (id, # of matches).
CREATE VIEW matchstat as 
select player.id, 
       count(match.id) as matches 
from player 
left join match 
on   player.id = winner 
  OR player.id =loser 
group by player.id;
