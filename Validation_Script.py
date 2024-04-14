from web3 import Web3
from hashlib import sha256
import json
from pymongo import MongoClient

# Connect to MongoDB Compass
client = MongoClient('mongodb+srv://archanvyas21:12345@mongodb.r1oetcg.mongodb.net/online_certificate')  # Update with your MongoDB Compass connection string
db = client['online_certificate']  # Update with your database name
collection = db['validation']  # Update with your collection name

# Connect to Ganache node
web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))  # Update with your Ganache node URL

# Load contract ABI and address
contract_address = "0x230368b2e4d93Cba584190127D35778A64DD03C7"  # Use the deployed contract address
with open('build/contracts/DocumentVerifier.json', 'r') as file:
    contract_data = json.load(file)
contract_abi = contract_data['abi']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function to store certificate hash in the blockchain
def store_certificate_hash(certificate_hash_bytes):
    try:
        # Specify the account address as the 'from' parameter
        account_address = "0xba0Ff0E852937209A7f4750875c4a7AB7f78cb91"  # Use your desired account address

        # Store certificate hash on the blockchain
        transaction_hash = contract.functions.addDocumentHash(certificate_hash_bytes).transact({'from': account_address})

        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

        return True
    except Exception as e:
        print(f"Error storing certificate hash: {e}")
        return False

# Function to validate certificate hash in the blockchain
def validate_certificate_hash(certificate_hash_bytes):
    try:
        # Retrieve stored hash from the blockchain
        print("Retrieving stored hash from the blockchain...")
        stored_hash = contract.functions.verifyDocumentHash(certificate_hash_bytes).call()

        # Compare retrieved hash with expected hash
        if stored_hash:
            print("Retrieved hash matches the expected hash.")
            return True
        else:
            print("Retrieved hash does not match the expected hash.")
            return False
    except Exception as e:
        print(f"Error validating certificate hash: {e}")
        return False

# Retrieve certificates from MongoDB Compass
cursor = collection.find({}, {'_id': False, 'certificate_hash': True})  # Assuming 'certificate_hash' is the field name storing certificate hashes

# Check if there are no certificates to retrieve
if cursor.count() == 0:
    print("No certificates found in the database.")
else:
    for document in cursor:
        try:
            # Calculate SHA-256 hash of the certificate
            certificate_hash = document['certificate_hash']

            # Convert hash to bytes
            certificate_hash_bytes = bytes.fromhex(certificate_hash)

            # Ensure hash is exactly 32 bytes long
            if len(certificate_hash_bytes) < 32:
                # Pad with zeros if shorter
                certificate_hash_bytes = certificate_hash_bytes.ljust(32, b'\0')
            elif len(certificate_hash_bytes) > 32:
                # Trim if longer
                certificate_hash_bytes = certificate_hash_bytes[:32]

            print(f"Processing certificate with hash: {certificate_hash}")

            # Store certificate hash in the blockchain
            if store_certificate_hash(certificate_hash_bytes):
                print("Certificate hash is stored in the blockchain.")
            else:
                print("Failed to store certificate hash in the blockchain.")

            # Validate certificate hash in the blockchain
            if validate_certificate_hash(certificate_hash_bytes):
                print("Certificate hash is validated in the blockchain.")
            else:
                print("Certificate hash is not validated in the blockchain.")
        except Exception as e:
            print(f"Error processing document: {e}")

# Close MongoDB Compass connection
client.close()
