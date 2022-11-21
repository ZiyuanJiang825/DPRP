from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for, session
import re
import psycopg2
import os
from web3 import Web3
from web3_config import *
from eth_account import Account
import secrets
from web3.gas_strategies.rpc import rpc_gas_price_strategy

app = Flask(__name__)

# in order to use session, we should assign a secret key to the app
app.secret_key = os.urandom(32).hex()

# set up database connection
conn = psycopg2.connect(
        host="localhost",
        database="dprp",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# set up web3 connection
w3 = Web3(Web3.HTTPProvider(WEB3_URL))
# set up default account
w3.eth.default_account = Account.from_key(ADMIN_PRIVATE_KEY)
# create the contract instance here
DPRP_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
# generate gas price strategy
w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

@app.route('/')
def start_redirect():
    return redirect(url_for("login"), code=302)

@app.route('/login', methods=('GET', 'POST'))
def login():
    msg = ''
    if request.method == 'POST' and 'inputUsername' in request.form and 'inputPassword' in request.form:
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['email'] = account[2]
            session['web3_account_pk'] = account[4]
            session['web3_account_addr'] = Account.from_key(account[4]).address
            msg = 'Logged in successfully !'
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/register', methods=('GET', 'POST'))
def register():
    msg = ''
    if request.method == 'POST' and 'inputUsername' in request.form and 'inputEmailAddress' in request.form \
            and 'inputPassword' in request.form and 'inputConfirmPassword' in request.form:
        username = request.form['inputUsername']
        password_1 = request.form['inputPassword']
        password_2 = request.form['inputConfirmPassword']
        email = request.form['inputEmailAddress']
        if username == '' or password_1 == '' or password_2 == '' or email == '':
            msg = 'Please fill out the form !'
            return render_template('register.html', msg=msg)

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not username.isalnum():
            msg = 'Username must contain only characters and numbers !'
        elif password_1 != password_2:
            msg = 'Password did not match! Please make sure they are the same!'
        elif not username or not password_1 or not password_2 or not email:
            msg = 'Please fill out the form !'
        else:
            new_pk = register_web3()
            withdraw(Account.from_key(new_pk).address, 0.01)
            cursor.execute('INSERT INTO users VALUES (DEFAULT, %s, %s, %s, %s)', (username, email, password_1, new_pk))
            conn.commit()
            msg = 'You have successfully registered !'
        cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

@app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/index')
def index():
    return render_template('index.html')

def register_web3():
    '''
    Register the account on the blockchain, send some coins to this account

    :return: account private key, account object
    '''
    priv = secrets.token_hex(32)
    new_acct_private_key = '0x' + priv
    return new_acct_private_key

def withdraw(addr, amount):
    '''

    :param addr: addr to receive the money
    :param amount: amount to transact. Unit: ether
    :return:
    '''
    withdraw_tx_hash = DPRP_contract.functions.withdraw(addr, Web3.toWei(0.01, 'ether')).build_transaction(
        {'gas': 100000,
         'gasPrice': w3.eth.generate_gas_price(),
         'nonce': w3.eth.get_transaction_count(w3.eth.default_account.address)
         })
    withdraw_signed_txn = w3.eth.default_account.sign_transaction(withdraw_tx_hash)
    w3.eth.send_raw_transaction(withdraw_signed_txn.rawTransaction)

if __name__ == '__main__':
    app.run(debug=True)
