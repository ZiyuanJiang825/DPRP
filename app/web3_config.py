# place to store some config values
# in development, please set these values to be your own values

# this should be changed for your own
CONTRACT_ADDRESS = '0x62a8b241624D251B43a6C7d0e62054f0435d7127'

# this should be changed for your own
CONTRACT_ABI = [
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
	}
]

# this should be changed for your own
ADMIN_PRIVATE_KEY = "185e104b52a687624e7e1045c254e2aa006f30b2b6df1b65cfa3c8bf493c1f92"

# your URL for web3 test server
WEB3_URL = 'HTTP://127.0.0.1:7545'