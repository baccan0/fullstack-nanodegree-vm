-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE player (id serial PRIMARY KEY, name varchar(40) NOT NULL);
CREATE TABLE match(id serial PRIMARY KEY, name varchar(40));
CREATE TABLE score(matchid integer REFERENCES match(id), playerid integer REFERENCES player(id), score integer, PRIMARY KEY(matchid,playerid) );
CREATE VIEW winstat as select id,count(score) as wins from player left join (select playerid,score from score where score =1) as wins on id = playerid group by id;
CREATE VIEW matchstat as select id, count(score) as matches from player left join score on id = playerid group by id;

