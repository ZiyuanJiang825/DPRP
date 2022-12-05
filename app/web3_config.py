# place to store some config values
# in development, please set these values to be your own values

# this should be changed for your own
CONTRACT_ADDRESS = '0x17b2c4a7AB870F5274d425DAB076d0D5d6cbbd5c'

# do not need to change it
CONTRACT_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "message",
                "type": "string"
            }
        ],
        "name": "Log",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "message",
                "type": "string"
            }
        ],
        "name": "addReview",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getBalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address payable",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]

# your URL for web3 test server
WEB3_URL = 'HTTP://127.0.0.1:7545'
