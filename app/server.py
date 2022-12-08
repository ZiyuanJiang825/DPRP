import json
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
from datetime import datetime

app = Flask(__name__)

# in order to use session, we should assign a secret key to the app
app.secret_key = os.environ['APP_SECRET_KEY']

# set up database connection
conn = psycopg2.connect(
    host="localhost",
    database="dprp",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'])

# set up web3 connection
w3 = Web3(Web3.HTTPProvider(WEB3_URL))
# set up default account
w3.eth.default_account = Account.from_key(os.environ['ADMIN_PRIVATE_KEY'])
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
    session.pop('web3_account_pk', None)
    session.pop('web3_account_addr', None)
    return redirect(url_for('login'))


@app.route('/index')
def index():
    if len(session) == 0:
        return redirect(url_for('login'))
    return render_template('index.html', id=session['id'])


@app.route('/reviews/<user_id>')
def myReview(user_id):
    if len(session) == 0:
        return redirect(url_for('login'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews WHERE user_id = %s', (user_id,))
    reviews = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('reviews.html', reviews=reviews)


@app.route('/products/all')
def allProducts():
    if len(session) == 0:
        return redirect(url_for('login'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('products.html', products=products)


@app.route('/add-review', methods=('GET', 'POST'))
def addReview():
    msg = ''
    if len(session) == 0:
        msg = 'Please Login First!'
        return render_template('add-review.html', msg=msg)
    accountId = str(session['id'])
    if request.method == 'POST' and 'inputTitle' in request.form and 'inputReview' in request.form \
            and 'inputProductName' in request.form and 'inputPros' in request.form \
            and 'inputCons' in request.form and request.form['inputRating'] != "Please Rate":
        title = request.form['inputTitle']
        productName = request.form['inputProductName']
        review = request.form['inputReview']
        pros = request.form['inputPros']
        cons = request.form['inputCons']
        rating = request.form['inputRating']
        if title == '' or productName == '' or review == '' or pros == '' or cons == '' or rating == 'Please Rate':
            msg = 'Please fill out the form !'
            return render_template('add-review.html', msg=msg)

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (accountId,))
        account = cursor.fetchone()
        if not account:
            msg = 'Account not found!'
        else:
            cursor.execute('SELECT * FROM products WHERE product_name  = %s', (productName,))
            product = cursor.fetchone()
            if not product:
                msg = 'Product not found!'
            else:
                productId = product[0]
                createTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                reviewEntry = {"title": title,
                               "productName": productName,
                               "userId": accountId,
                               "review": review,
                               "pros": pros,
                               "cons": cons,
                               "rating": rating,
                               "create_time": createTime
                               }
                reviewjson = json.dumps(reviewEntry)
                txHash = addReview(session['web3_account_pk'], session['web3_account_addr'], reviewjson)
                cursor.execute('INSERT INTO reviews\
                                 VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING review_id', \
                               (
                               accountId, w3.toHex(txHash), title, productName, review, pros, cons, rating, createTime))
                [reviewId] = cursor.fetchone()
                cursor.execute('INSERT INTO product2reviews\
                                 VALUES (%s, %s)', \
                               (productId, reviewId))
                cursor.execute('''
                INSERT INTO review_histories
                VALUES(%s, %s, %s)
                ''', (w3.toHex(txHash), reviewId, createTime))
                conn.commit()
                msg = 'You have successfully added a review!'
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('add-review.html', msg=msg)


@app.route('/reviews/edit/<review_id>')
def editReview(review_id):
    msg = ''
    if len(session) == 0:
        return
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews WHERE review_id = %s', (review_id,))
    review = cursor.fetchone()
    reviewEntry = {"Id": review[0],
                   "Title": review[3],
                   "ProductName": review[4],
                   "Review": review[5],
                   "Pros": review[6],
                   "Cons": review[7],
                   "Rating": review[8],
                   "Create_time": review[9]
                   }
    conn.commit()
    cursor.close()

    return render_template('edit-review.html', review=reviewEntry, msg='')


@app.route('/reviews/edit/<review_id>/submit', methods=('GET', 'POST'))
def editSubmitReview(review_id):
    msg = ''
    if len(session) == 0:
        msg = 'Please Login First!'
        return render_template('edit-review.html', msg=msg)
    accountId = str(session['id'])
    print(request.method)
    print(request.form)
    if request.method == 'POST' and 'inputTitle' in request.form and 'inputReview' in request.form \
            and 'inputProductName' in request.form and 'inputPros' in request.form \
            and 'inputCons' in request.form and request.form['inputRating'] != "Please Rate":
        title = request.form['inputTitle']
        productName = request.form['inputProductName']
        review = request.form['inputReview']
        pros = request.form['inputPros']
        cons = request.form['inputCons']
        rating = request.form['inputRating']
        if title == '' or productName == '' or review == '' or pros == '' or cons == '' or rating == 'Please Rate':
            msg = 'Please fill out the form !'
            return render_template('edit-review.html', msg=msg, review={"Id": review_id})

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (accountId,))
        account = cursor.fetchone()
        if not account:
            msg = 'Account not found!'
        else:
            cursor.execute('SELECT * FROM products WHERE product_name  = %s', (productName,))
            product = cursor.fetchone()
            if not product:
                msg = 'Product not found!'
            else:
                productId = product[0]
                createTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                reviewEntry = {"Id": review_id,
                               "title": title,
                               "productName": productName,
                               "userId": accountId,
                               "review": review,
                               "pros": pros,
                               "cons": cons,
                               "rating": rating,
                               "create_time": createTime
                               }
                reviewjson = json.dumps(reviewEntry)
                txHash = addReview(session['web3_account_pk'], session['web3_account_addr'], reviewjson)
                cursor.execute('''
                UPDATE reviews
                SET tx_hash=%s, title=%s, product_name=%s, review=%s, pros=%s, cons=%s, rating=%s, create_time=%s
                where review_id=%s
                ''', (w3.toHex(txHash), title, productName, review, pros, cons, rating, createTime, review_id))

                cursor.execute('''
                INSERT INTO review_histories
                VALUES(%s, %s, %s)
                ''', (w3.toHex(txHash), review_id, createTime))
                conn.commit()
                msg = 'You have successfully edited a review!'
                return render_template('edit-review.html', msg=msg, review=reviewEntry)
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('edit-review.html', msg=msg, review='')


@app.route('/review/<user_id>/<review_id>', methods=['GET', 'POST'])
def review(user_id, review_id):
    if len(session) == 0:
        return redirect(url_for('login'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews WHERE user_id = %s and review_id = %s', (user_id, review_id,))
    review = cursor.fetchone()
    cursor.execute('SELECT * FROM review_histories WHERE review_id = %s ORDER BY create_time ASC', (review_id,))
    editHistory = cursor.fetchall()
    print(editHistory)
    reviewEntry = {"Id": review[0],
                   "Title": review[3],
                   "ProductName": review[4],
                   "Review": review[5],
                   "Pros": review[6],
                   "Cons": review[7],
                   "Rating": review[8],
                   "Create_time": review[9]
                   }
    conn.commit()
    cursor.close()
    return render_template('review.html', review=reviewEntry, editHistory=editHistory)


@app.route('/review/verify', methods=['POST'])
def verify():
    reviewId = request.get_json()['Id']
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews WHERE review_id = %s', (reviewId,))
    review = cursor.fetchone()
    reviewEntry = {"title": review[3],
                   "productName": review[4],
                   "userId": str(review[1]),
                   "review": review[5],
                   "pros": review[6],
                   "cons": review[7],
                   "rating": str(review[8]),
                   "create_time": review[9]
                   }
    reviewjson = json.dumps(reviewEntry)
    hashedjson = str(w3.keccak(text=reviewjson))
    reviewTxHash = review[2]
    tx_receipt = w3.eth.get_transaction_receipt(reviewTxHash)
    review_details = DPRP_contract.events.Log().processLog(tx_receipt['logs'][0])
    conn.commit()
    cursor.close()
    if hashedjson == review_details['args']['message']:
        return jsonify('This review is valid!')
    else:
        return jsonify('This review is corrupted!')


@app.route('/product/<product_id>', methods=['GET', 'POST'])
def view_proudct(product_id):
    # first we need to retrieve the product info
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
    product = cursor.fetchone()
    productEntry = {"Id": product[0],
                    "Name": product[1],
                    "Link": product[2],
                    "Description": product[3],
                    }
    conn.commit()
    cursor.close()

    # then we need to retrieve all the reviews related to this product
    cursor = conn.cursor()
    cursor.execute('''
        WITH reviewTable (review_id) AS (
                SELECT review_id FROM product2reviews
                WHERE product_id = %s 
        )
            SELECT reviews.title, reviews.review, reviews.pros, reviews.cons, reviews.rating, users.username
            FROM reviewTable
            JOIN reviews
            ON reviews.review_id=reviewTable.review_id 
            JOIN users
            ON users.id=reviews.user_id
    ''', (product_id,))
    reviews = cursor.fetchall()
    print(reviews)
    conn.commit()
    cursor.close()
    return render_template('product.html', product=productEntry, reviews=reviews)


@app.route('/add-product', methods=('GET', 'POST'))
def addProduct():
    msg = ''
    if len(session) == 0:
        msg = 'Please Login First!'
        return render_template('add-product.html', msg=msg)
    accountId = str(session['id'])
    if request.method == 'POST' and 'inputProductName' in request.form and 'inputLink' in request.form \
            and 'inputDescript' in request.form:
        productName = request.form['inputProductName']
        link = request.form['inputLink']
        descript = request.form['inputDescript']
        if productName == '' or link == '' or descript == '':
            msg = 'Please fill out the form !'
            return render_template('add-product.html', msg=msg)

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (accountId,))
        account = cursor.fetchone()
        if not account:
            msg = 'Account not found!'
        else:
            cursor.execute('SELECT * FROM products WHERE product_name  = %s', (productName,))
            product = cursor.fetchone()
            if product:
                msg = 'Product already exists!'
            else:
                cursor.execute('INSERT INTO products\
                                 VALUES (DEFAULT, %s, %s, %s)', (productName, link, descript))
                conn.commit()
                msg = 'You have successfully added a product!'
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('add-product.html', msg=msg)


@app.route('/search')
def search():
    return render_template('search.html', products=[])


@app.route('/search/<searchText>', methods=('GET', 'POST'))
def performSearch(searchText):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE product_name LIKE %s', ('%' + searchText + '%',))
    products = cursor.fetchall()
    conn.commit()
    cursor.close()
    return jsonify(products)


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
    withdraw_tx_hash = DPRP_contract.functions.withdraw(addr, Web3.toWei(amount, 'ether')).build_transaction(
        {'gas': 100000,
         'gasPrice': w3.eth.generate_gas_price(),
         'nonce': w3.eth.get_transaction_count(w3.eth.default_account.address)
         })
    withdraw_signed_txn = w3.eth.default_account.sign_transaction(withdraw_tx_hash)
    w3.eth.send_raw_transaction(withdraw_signed_txn.rawTransaction)


def addReview(pk, addr, msg):
    '''

    :param addr: addr to receive the money
    :param amount: amount to transact. Unit: ether
    :return:
    '''
    hashedMsg = str(w3.keccak(text=msg))
    review_tx = DPRP_contract.functions.addReview(hashedMsg).build_transaction(
        {
            'nonce': w3.eth.get_transaction_count(addr)
        })
    review_signed_txn = w3.eth.account.sign_transaction(review_tx, pk)
    review_tx_hash = w3.eth.send_raw_transaction(review_signed_txn.rawTransaction)
    return review_tx_hash


if __name__ == '__main__':
    app.run(debug=True)
