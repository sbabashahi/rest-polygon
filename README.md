This is a practicing project. I just tried to learn how geo works in django and postgres.

**Initial Postgres DB**

**CREATE DB**

sudo su postgres -> psql -> CREATE DATABASE geodb; -> CREATE USER geo WITH PASSWORD 'Ge0dB'; -> 
ALTER ROLE geo SET client_encoding TO 'utf8'; -> ALTER ROLE geo SET default_transaction_isolation TO 'read committed'; 
-> ALTER ROLE geo SET timezone TO 'UTC';



**GEO installations**

sudo apt-get install binutils libproj-dev gdal-bin

sudo apt install postgis

-> psql geodb  -> CREATE EXTENSION postgis;
