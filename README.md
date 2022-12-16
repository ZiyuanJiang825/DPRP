# Overview

DPRP is a Decentralized Product Review Platform.

## Teammates

- Ziyuan Jiang (zj2322)

- Jiarui Lyu (jl6038)

- Kerim Kurttepeli (kk3084)

## Features
- Review features including adding, viewing, and verifying a review are added. Please checkout feature/review branch
- Product and product2reviews tables are added in local db for review test. (A product named 'ipad' is pre-inserted for review test)

  

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

### Step 4: Set environment variable for database encryption

Generate a key for encryption, and store it as `DB_KEY` for env variable.
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
```

Note:

[PgAdmin 4](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v6.16/macos/) is a good tool to manage the PostgreSQL.

  

## Web3 setup

To setup the web3 development environment, follow the steps below:

### Step 0: Create your own web3_config.py
Every developer needs to maintain a `web3_config.py` file in order to run the app. The script should be
at `DPRP/app/web3_configy.py`.

### Step 1: Connect to a blockchain

Use Ganache-cli or Ganache app to create a testnet. Get the url of the testnet, copy and paste it to `WEB3_URL` in `web3_config.py`.

  

### Step 2: Configure the admin account

Choose one account in the testnet as the admin account, set environment variable `ADMIN_PRIVATE_KEY` as the private key
of this account.

  

### Step 3: Configure the contract

The contract is in `contracts/DPRP.sol`. Use Remix IDE to deploy the contract to Ganache provider (you should use the admin account to deploy the contract). Copy and paste the contract address and its ABI to `web3_config.py`.

  

### Step 4: Initialize the contract

Initialize the contract by sending some money to the contract. This can be done by running `web3_init.py`.

### Example
An example of `web3_config.py` should look like:
```python
# place to store some config values
# in development, please set these values to be your own values

# this should be changed for your own
CONTRACT_ADDRESS = 'XXXXXXXXXXXXX'

# this should be changed for your own
CONTRACT_ABI = ["XXXXXXX"]

# your URL for web3 test server
WEB3_URL = 'HTTP://127.0.0.1:7545'
```

# Production
We will deploy our app to Heroku.

## Heroku Setup

### Step 1: Install Git and Heroku CLI
Assume you already have Git, then refer to this [page](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli) for Heroku CLI installation.

### Step 2: Login to Heroku
```shell
heroku login
```
Make sure you login to Heroku. 

### Step 3: Create a Heroku Remote
Follow this [step](https://devcenter.heroku.com/articles/git#create-a-heroku-remote).

### Step 4: Configure Procfile
Reference: https://devcenter.heroku.com/articles/procfile

## Database Setup
_Reference: https://devcenter.heroku.com/articles/connecting-heroku-postgres_

Heroku naturally supports PostgreSQL. So we will need to configure the database, and make it connect to the remote database.
**BEFORE** continue, make sure you already configure your local postgre setting (can be found in development guide part).

### Step 1: Create database on Heroku
```shell
heroku addons:create heroku-postgresql:mini
```

### Step 2: Get the username and password for the database
```shell
heroku pg:credentials:url DATABASE
```

### Step 3: Set the configure in Python
Refer to this [step](https://devcenter.heroku.com/articles/connecting-heroku-postgres#connecting-in-python)

After that, you can rerun `db_init.py` to test if the connection works.

## Web3 Setup
We will use Goerli test network as our blockchain network.

### Step 1: Set up an admin account and request some coins
Go to Metamask, create an account, and then go to this [website](https://goerlifaucet.com/
) to request some coins daily. Set the private key of admin in `web3_config.py`.

### Step 2: Get the API of testnet
Register an account and a project on Infura, use its Goerli API address, change accordingly in `web3_config.py`

### Step 3: Deploy the contract via Remix
Change the provider to Injected Provider - MetaMask, deploy the contract and copy the contract address to `web3_config.py`.

### Step 4: Run `web3_init.py`
## Set environment variables on Heroku
```shell
heroku config:set DATABASE_URL=xxxx
heroku config:set APP_SECRET_KEY=xxxx
heroku config:set DB_KEY=xxxx
```
For the secret key, use `os.urandom(32).hex()` to generate.