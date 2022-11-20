# Overview
DPRP is a Decentralized Product Review Platform.
## Teammates
- Ziyuan Jiang (zj2322)
- Jiarui Lyu ()
- Kerim Kurttepeli ()

# Development Guide
## Database Setup
We will use PostgreSQL for our project. Please follow the steps below to setup you database environment locally.
### Step 1: Install PostgreSQL
First, install postgresql using homebrew:
```
brew install postgresql
```
This will create a default server, and the username is `postgres`. And then start the server:
```
brew services start postgresql
```

### Step 2: Create database for our project
Let's go into the server first.
```
psql postgres
```
Create a database for our project:
```
CREATE DATABASE DPRP;
```
Create a user for our project:
```
CREATE USER sammy WITH PASSWORD 'password';
```
Give the new user the access to our database:
```
GRANT ALL PRIVILEGES ON DATABASE flask_db TO sammy;
```
Confirm our database has been created:
```
\l
```
If you can see the database you created, enter `\q` to leave.

Finally, store the username and password as your environment variables:
```
export DB_USERNAME = 'sammy';
export DB_PASSWORD = 'password';
```


### Step 3: Use PostgreSQL in Flask app
Run `db_init.py` to create all the tables that is needed for our project. If you are using IDE like PyCharm, remember to configure the environment variables before running the script.

Note: 
[PgAdmin 4](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v6.16/macos/) is a good tool to manage the PostgreSQL.

# Production

