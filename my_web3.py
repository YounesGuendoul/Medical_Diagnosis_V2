from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/623b6ab0286a4952a6247eb9b38ee288"))
contract_address = "0x792680aB"
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_interactionData",
				"type": "string"
			}
		],
		"name": "addInteraction",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "authorizeUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "revokeUser",
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
				"internalType": "uint256",
				"name": "interactionIndex",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "interactionData",
				"type": "string"
			}
		],
		"name": "InteractionAdded",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "UserAuthorized",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "UserRevoked",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "authorizedUsers",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "chatbotInteractions",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "interactionData",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "getInteraction",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getInteractionCount",
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
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

sender_address = "0xa"
private_key = "8d"

def add_chatbot_interaction(user, interaction_data):
    # Prepare and send a transaction to add an interaction
    nonce = w3.eth.getTransactionCount(sender_address)
    gas_price = w3.toWei("20", "gwei")  # Adjust gas price as needed
    gas_limit = 200000  # Adjust gas limit as needed

    transaction = contract.functions.addInteraction(interaction_data).buildTransaction({
        'chainId': 1,  # Mainnet
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
    })

    signed_transaction = w3.eth.account.signTransaction(transaction, private_key=private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return tx_hash.hex()


def get_chatbot_interactions():
    # Get the total number of interactions
    interaction_count = contract.functions.getInteractionCount().call()

    # Initialize a list to store the interactions
    interactions = []

    # Retrieve each interaction one by one
    for index in range(interaction_count):
        # Retrieve the interaction details by index
        interaction_details = contract.functions.getInteraction(index).call()

        # Add the interaction details to the list
        interactions.append({
            "timestamp": interaction_details[0],
            "user": interaction_details[1],
            "interaction_data": interaction_details[2]
        })

    return interactions

