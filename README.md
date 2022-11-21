# Overview
DPRP is a Decentralized Product Review Platform.
## Teammates
- Ziyuan Jiang (zj2322)
- Jiarui Lyu (jl6038)
- Kerim Kurttepeli (kk3084)

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
Run `db_init.py` to create all the tables that is needed for our project. If you are using IDE like PyCharm, remember to configure the environment variables (username and password) before running the script.

Note: 
[PgAdmin 4](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v6.16/macos/) is a good tool to manage the PostgreSQL.

## Web3 setup
To setup the web3 development environment, follow the steps below:

### Step 1: Connect to a blockchain
Use Ganache-cli or Ganache app to create a testnet. Get the url of the testnet, copy and paste it to `WEB3_URL` in `web3_config.py`.

### Step 2: Configure the admin account
Choose one account in the testnet as the admin account, copy and paste its private key in `web3_config.py`.

### Step 3: Configure the contract
The contract is in `contracts/DPRP.sol`. Use Remix IDE to deploy the contract to Ganache provider (you should use the admin account to deploy the contract). Copy and paste the contract address and its ABI to `web3_config.py`.

### Step 4: Initialize the contract
Initialize the contract by sending some money to the contract. This can be done by running `web3_init.py`.

# Production

