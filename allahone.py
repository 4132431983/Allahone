from web3 import Web3
import json
import time

# Set up your Alchemy provider URL (replace with your Alchemy URL)
ALCHEMY_URL = 'https://eth-mainnet.alchemyapi.io/v2/qA9FV5BMTFx6p7638jhqx-JDFDByAZAn'  # Replace with your Alchemy API key
web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

# Your Ethereum wallet addresses and private keys
wallet_address = '0x4DE23f3f0Fb3318287378AdbdE030cf61714b2f3'  # The address you are sending from
gas_fee_payer_private_key = '0x8b958d58f7fd14d1becf61a9805a5168e1c34d50ef1f15c0198730996485af8b'  # The private key to pay gas fees
destination_address = '0x5d1fc5b5090c7ee9e81a9e786a821b8281ffe582'  # The destination wallet address
usdt_contract_address = '0xdac17f958d2ee523a2206206994597c13d831ec7'  # USDT ERC-20 contract on Ethereum

# USDT contract ABI for the transfer function
usdt_abi = json.loads('[{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

# USDT transfer function
usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_abi)

# Convert USDT amount to the correct number of decimals
usdt_amount = 2200
usdt_decimals = 6  # USDT has 6 decimals
usdt_amount_in_wei = int(usdt_amount * (10 ** usdt_decimals))

# Function to get current gas price
def get_gas_price():
    gas_price = web3.eth.gas_price
    return gas_price

# Function to check if the balance is enough for transaction
def check_balance(wallet_address, required_balance_in_eth):
    balance = web3.eth.get_balance(wallet_address)
    if balance < required_balance_in_eth:
        return False
    return True

# Function to send USDT
def send_usdt():
    # Estimate gas for the transaction
    gas_price = get_gas_price()
    estimated_gas = usdt_contract.functions.transfer(destination_address, usdt_amount_in_wei).estimateGas({'from': wallet_address})

    # Check if the gas fee payer has enough ETH to cover the gas
    gas_fee = gas_price * estimated_gas
    required_eth_balance = gas_fee / 10**18  # Convert Wei to ETH

    # Make sure gas payer has enough ETH
    if not check_balance(wallet_address, required_eth_balance):
        print("Error: Not enough ETH for gas fees.")
        return

    # Create the transaction
    tx = usdt_contract.functions.transfer(destination_address, usdt_amount_in_wei).buildTransaction({
        'chainId': 1,  # Mainnet
        'gas': estimated_gas,
        'gasPrice': gas_price,
        'nonce': web3.eth.getTransactionCount(wallet_address),
    })

    # Sign the transaction with the gas fee payer private key
    signed_tx = web3.eth.account.signTransaction(tx, gas_fee_payer_private_key)

    # Send the transaction
    try:
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Transaction sent successfully! TX Hash: {web3.toHex(tx_hash)}")

        # Wait for the transaction to be mined
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        if receipt['status'] == 1:
            print("\033[92mTransaction confirmed and successfully sent!\033[0m")  # Green color for success
        else:
            print("Transaction failed.")
    except Exception as e:
        print(f"Error sending transaction: {str(e)}")

# Ensure gas is enough to send the transaction with a buffer of 0.005 ETH for gas fees
gas_buffer_eth = 0.005  # ETH buffer for gas fees
if check_balance(wallet_address, gas_buffer_eth):
    send_usdt()
else:
    print(f"Error: Not enough ETH for gas fees. At least {gas_buffer_eth} ETH required.")