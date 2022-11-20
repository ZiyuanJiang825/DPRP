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
https://www.postgresql.org/ftp/pgadmin/pgadmin4/v6.16/macos/

# Production

