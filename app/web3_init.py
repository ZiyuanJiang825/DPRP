# get the gas price
from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3_config import *
from eth_account import Account
import os

w3 = Web3(Web3.HTTPProvider(WEB3_URL))
w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

w3.eth.default_account = Account.from_key(os.environ['ADMIN_PRIVATE_KEY'])

'''
Send some money from admin account to the contract
'''

# signed the transaction
signed_txn = w3.eth.default_account.sign_transaction(dict(
    nonce=w3.eth.get_transaction_count(w3.eth.default_account.address),
    gas=100000,
    gasPrice=w3.eth.generate_gas_price(),
    to=CONTRACT_ADDRESS,
    value=Web3.toWei(0.4, 'ether')
  ))
w3.eth.send_raw_transaction(signed_txn.rawTransaction)