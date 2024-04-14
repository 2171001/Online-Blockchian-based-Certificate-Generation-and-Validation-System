import json

# Load contract ABI from JSON file
with open('/home/voldemort/Music/Documents/Project_G29/Truffle/Document validation using Blockchain/build/contracts/DocumentVerifier.json', 'r') as file:
    contract_abi = json.load(file)
