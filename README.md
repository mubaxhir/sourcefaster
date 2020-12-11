# Login-Flask
Login Page made in Flask, HTML and CSS using Sqlite.

## Instructions to Run :
#### NOTE : I tested this on WINDOWS. So do check other platform instructions if you need to. Mostly these steps are same for all OS.
1. Download [Sqlite](https://www.sqlite.org/download.html) . This repo already having those file so no need to download them again.
   - NOTE : Please Note that I tested this on windows platform. Please do check instructions for other OS if you need so.
2. Now, Use these commands to run this database.
```
sqlite3 database.db < schema.sql
sqlite3
```
##### Now, "sqlite>" will show in terminal. Now, use these commands to check the contents of table.
```
.open database.db
create table users ( id integer PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL);
select * from users;
```
###### To add a used from terminal, use this command
```
INSERT INTO table_name (
 column1,
 column2 ,..)
VALUES
 (
 value1,
 value2 ,...);
```

#### for starting please install the following libraries:
pip install Flask
pip install shuttle 
pip install PyVirtualDisplay
pip install selenium
pip install googletrans
pip install tox

###### for Running run command:
*$ python app.py*
