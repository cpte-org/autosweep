import time
import datetime
import os
import logging
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account import Account

load_dotenv()  # take environment variables from .env.

# Ethereum network endpoint and project ID
rpc_endpoint = os.environ.get('RPC_ENDPOINT')
w3 = Web3(HTTPProvider(rpc_endpoint))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Account private key and recipient address
private_key = os.environ.get('PRIV_KEY')
recipient_address = w3.toChecksumAddress(os.environ.get('RCVING_ADDR'))

# Gas price and limit for the transaction
gas_price = w3.eth.gas_price
gas_limit = 21000

# Configure logging to a file
logging.basicConfig(filename='./sweeper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sweep_account_balance():
    # Get the current account balance
    account = Account.privateKeyToAccount(private_key)
    balance = w3.eth.get_balance(account.address)

    # Calculate the transaction fee and amount to send (full balance minus transaction fee)
    transaction_fee = gas_price * gas_limit
    eth_to_send = balance - transaction_fee

    # Send the transaction to the recipient address
    if eth_to_send > 0:
        message = f"Sending {w3.fromWei(eth_to_send, 'ether')} ETH to {recipient_address}..."
        print(message)
        logging.info(message)
        # Build and sign the transaction
        transaction = {
            'to': recipient_address,
            'value': eth_to_send,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': w3.eth.getTransactionCount(account.address),
        }
        signed_tx = account.signTransaction(transaction)

        # Send the signed transaction
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        message = f"Transaction sent with hash: {tx_hash.hex()}."
        print(message)
        logging.info(message)

        # Wait for confirmation and retrieve the transaction receipt
        message = "Waiting for transaction confirmation..."
        print(message)
        logging.info(message)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        message = f"Transaction confirmed with status: {tx_receipt.status}."
        print(message)
        logging.info(message)
        message = f"Transaction hash: {tx_receipt.transactionHash.hex()}."
        print(message)
        logging.info(message)
    else:
        message = f"Account balance is {w3.fromWei(balance, 'ether')} ETH, which is not enough to cover the transaction fee."
        print(message)
        logging.info(message)

# Sweep the account balance every 20 seconds
while True:
    sweep_account_balance()
    ct = datetime.datetime.now()
    message = "Sweeping account balance at {}".format(ct)
    print(message)
    logging.info(message)
    time.sleep(20)
