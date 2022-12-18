from flask import Response, session, jsonify
from server import app, db_key
import psycopg2
import unittest
import os
from cryptography.fernet import Fernet
from eth_account import Account
from web3 import Web3
from web3_config import *
import json

class Flasktest(unittest.TestCase):
    def test_01_register_success(self):
        tester = app.test_client(self)
        username = "1"
        password = "password"
        emailAddress = "1@gmail.com"
        response = tester.post('/register', data = {
            "inputUsername": username,
            "inputPassword": password,
            "inputConfirmPassword": password,
            "inputEmailAddress": emailAddress
        })
        self.assertEqual(response.status_code, 200)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        self.assertEqual(account[1], username)
        self.assertEqual(account[2], emailAddress)
        self.assertEqual(fernet.decrypt(bytes(account[3])).decode('utf-8'), password)
        accountPK = fernet.decrypt(bytes(account[4])).decode('utf-8')
        accountAddress = Account.from_key(accountPK).address
        self.assertGreater(w3.eth.getBalance(accountAddress),0)

    def test_02_register_failure_unmatchedPassword(self):
        tester = app.test_client(self)
        username = "2"
        password = "password"
        emailAddress = "1@gmail.com"
        response = tester.post('/register', data = {
            "inputUsername": username,
            "inputPassword": password,
            "inputConfirmPassword": "123",
            "inputEmailAddress": emailAddress
        })
        self.assertEqual(response.status_code, 200)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        self.assertEqual(account, None)
    
    def test_03_register_failure_missingInfo(self):
        tester = app.test_client(self)
        username = "2"
        password = "password"
        emailAddress = "1@gmail.com"
        response = tester.post('/register', data = {
            "inputUsername": username,
            "inputPassword": password,
            "inputConfirmPassword": "123",
        })
        self.assertEqual(response.status_code, 200)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        self.assertEqual(account, None)

    def test_04_register_failure_invalidEmail(self):
        tester = app.test_client(self)
        username = "2"
        password = "password"
        emailAddress = "1gmail.com"
        response = tester.post('/register', data = {
            "inputUsername": username,
            "inputPassword": password,
            "inputConfirmPassword": "123",
            "inputEmailAddress": emailAddress
        })
        self.assertEqual(response.status_code, 200)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        self.assertEqual(account, None)
    
    def test_05_register_failure_invalidUsername(self):
        tester = app.test_client(self)
        username = "2.."
        password = "password"
        emailAddress = "1@gmail.com"
        response = tester.post('/register', data = {
            "inputUsername": username,
            "inputPassword": password,
            "inputConfirmPassword": "123",
            "inputEmailAddress": emailAddress
        })
        self.assertEqual(response.status_code, 200)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        self.assertEqual(account, None)
    
    def test_06_login_success(self):
        tester = app.test_client(self)
        with tester:
            username = "1"
            password = "password"
            response = tester.post('/login', data = {
                "inputUsername": username,
                "inputPassword": password,
            })
            self.assertEqual(session['username'], username)
            self.assertGreater(w3.eth.getBalance(session['web3_account_addr']),0)

    def test_07_login_failure(self):
        tester = app.test_client(self)
        with tester:
            username = "2"
            password = "password"
            response = tester.post('/logout')
            response = tester.post('/login', data = {
                "inputUsername": username,
                "inputPassword": password,
            })
            self.assertEqual(len(session), 0)
    
    def test_08_add_product(self):
        tester = app.test_client(self)
        username = "1"
        password = "password"
        tester.post('/login', data = {
            "inputUsername": username,
            "inputPassword": password,
        })
        productName = "iphone"
        inputLink = "www.test.com"
        inputDescription = "test"
        tester.post('/add-product', data = {
            "inputProductName": productName,
            "inputLink": inputLink,
            "inputDescript":inputDescription,
        })
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE product_name = %s', (productName,))
        product = cursor.fetchone()
        self.assertEqual(product[2], inputLink)
        self.assertEqual(product[3], inputDescription)

    def test_09_add_review_success(self):
        tester = app.test_client(self)
        username = "1"
        password = "password"
        tester.post('/login', data = {
            "inputUsername": username,
            "inputPassword": password,
        })
        title = "test"
        productName = "ipad"
        content = "test"
        pros = "test"
        cons = "test"
        rating = "2"
        tester.post('/add-review', data = {
            "inputTitle": title,
            "inputProductName": productName,
            "inputReview": content,
            "inputPros":pros,
            "inputCons": cons,
            "inputRating": rating,
        })
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reviews WHERE title  = %s', (title,))
        review = cursor.fetchone()
        self.assertEqual(review[4], productName)
        self.assertEqual(review[5], content)
        self.assertEqual(review[6], pros)
        self.assertEqual(review[7], cons)
        self.assertEqual(review[8], int(rating))
    
    def test_10_add_review_failureNoProduct(self):
        tester = app.test_client(self)
        username = "1"
        password = "password"
        tester.post('/login', data = {
            "inputUsername": username,
            "inputPassword": password,
        })
        title = "test_imac"
        productName = "imac"
        content = "test"
        pros = "test"
        cons = "test"
        rating = "2"
        tester.post('/add-review', data = {
            "inputTitle": title,
            "inputProductName": productName,
            "inputReview": content,
            "inputPros":pros,
            "inputCons": cons,
            "inputRating": rating,
        })
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reviews WHERE title  = %s', (title,))
        review = cursor.fetchone()
        self.assertEqual(review, None)
    
    def test_11_security_add_review_failureNoPurchase(self):
        tester = app.test_client(self)
        username = "1"
        password = "password"
        tester.post('/login', data = {
            "inputUsername": username,
            "inputPassword": password,
        })
        productName = "ipod"
        inputLink = "www.test.com"
        inputDescription = "test"
        tester.post('/add-product', data = {
            "inputProductName": productName,
            "inputLink": inputLink,
            "inputDescript":inputDescription,
        })
        productName = "itouch"
        tester.post('/add-product', data = {
            "inputProductName": productName,
            "inputLink": inputLink,
            "inputDescript":inputDescription,
        })
        title = "test_ipod"
        productName = "itouch"
        content = "test"
        pros = "test"
        cons = "test"
        rating = "2"
        tester.post('/add-review', data = {
            "inputTitle": title,
            "inputProductName": productName,
            "inputReview": content,
            "inputPros":pros,
            "inputCons": cons,
            "inputRating": rating,
        })
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reviews WHERE title  = %s', (title,))
        review = cursor.fetchone()
        self.assertEqual(review, None)

    def test_12_verify(self):
        tester = app.test_client(self)
        username = "1"
        password = "password"
        tester.post('/login', data = {
            "inputUsername": username,
            "inputPassword": password,
        })
        rsp = tester.post('/review/verify', data = json.dumps(dict(Id="1")), content_type='application/json')
        self.assertEqual(rsp.data, b'"This review is valid!"\n')
        cursor = conn.cursor()
        cursor.execute('UPDATE reviews SET title = %s WHERE review_id  = %s', ("corrupted","1"))
        conn.commit()
        cursor.close()
        rsp = tester.post('/review/verify', data = json.dumps(dict(Id="1")), content_type='application/json')
        self.assertEqual(rsp.data, b'"This review is corrupted!"\n')
        conn.commit()
        cursor.close()
        cursor = conn.cursor()
        cursor.execute('UPDATE reviews SET title = %s WHERE review_id  = %s', ("test","1"))
        conn.commit()
        cursor.close()
    
    def test_13_edit_review(self):
        tester = app.test_client(self)
        username = "1"
        password = "password"
        tester.post('/login', data = {
            "inputUsername": username,
            "inputPassword": password,
        })
        title = "edited"
        productName = "ipad"
        content = "edited"
        pros = "edited"
        cons = "edited"
        rating = "3"
        tester.post('/reviews/edit/1/submit', data = {
            "inputTitle": title,
            "inputProductName": productName,
            "inputReview": content,
            "inputPros":pros,
            "inputCons": cons,
            "inputRating": rating,
        })
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reviews WHERE review_id  = %s', (1,))
        review = cursor.fetchone()
        self.assertEqual(review[3], title)
        self.assertEqual(review[4], productName)
        self.assertEqual(review[5], content)
        self.assertEqual(review[6], pros)
        self.assertEqual(review[7], cons)
        self.assertEqual(review[8], int(rating))
        rsp = tester.post('/review/verify', data = json.dumps(dict(Id="1")), content_type='application/json')
        self.assertEqual(rsp.data, b'"This review is valid!"\n')





        



if __name__ == '__main__':
    exec(open("web3_init.py").read())
    exec(open("db_init.py").read())
    # set up database connection
    conn = psycopg2.connect(
            host="localhost",
            database="dprp",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    fernet = Fernet(db_key)
    w3 = Web3(Web3.HTTPProvider(WEB3_URL))
    unittest.main()
    conn.close()