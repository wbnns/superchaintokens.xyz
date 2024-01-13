import json
import requests
from datetime import datetime

def fetch_and_process_json(url, output_names):
    # Fetch the JSON data from the URL
    response = requests.get(url)
    data = response.json()

    # Split the tokens by 'chainId'
    tokens_by_chainid = {}
    for token in data['tokens']:
        chain_id = token['chainId']
        if chain_id not in tokens_by_chainid:
            tokens_by_chainid[chain_id] = []
        tokens_by_chainid[chain_id].append(token)

    # Process each chainId group
    for chain_id, new_tokens in tokens_by_chainid.items():
        if chain_id in output_names:
            output_file_name = output_names[chain_id]
            output_file_path = f'./{output_file_name}'  # Update this path as needed
            
            existing_tokens = []
            # Check if the file already exists
            try:
                with open(output_file_path, 'r') as existing_file:
                    existing_data = json.load(existing_file)
                    existing_tokens = existing_data.get('tokens', [])
            except FileNotFoundError:
                pass  # File doesn't exist, will be created

            # Update existing data with new tokens
            updated_tokens, duplicates = update_tokens(existing_tokens, new_tokens)

            # Sort tokens alphabetically by 'name'
            updated_tokens.sort(key=lambda x: x.get('name', '').lower())

            # Update the data structure with the new tokens list
            updated_data = data.copy()
            updated_data['tokens'] = updated_tokens

            # Write the updated data to the file
            with open(output_file_path, 'w') as outfile:
                json.dump(updated_data, outfile, indent=2)

def update_tokens(existing_tokens, new_tokens):
    # Create a dictionary of existing tokens by their address for quick lookup
    existing_tokens_dict = {token['address']: token for token in existing_tokens}
    duplicates = []

    for token in new_tokens:
        address = token['address']
        # Add new token if it doesn't exist; else, log and mark as a duplicate
        if address in existing_tokens_dict:
            print(f"Duplicate token found: {token['name']} has the same address as {existing_tokens_dict[address]['name']}")
            duplicates.append((token['name'], existing_tokens_dict[address]['name']))
        else:
            existing_tokens_dict[address] = token

    # Convert the dictionary back to a list and mark duplicates
    updated_tokens_list = []
    for address, token in existing_tokens_dict.items():
        if any(dup[0] == token['name'] for dup in duplicates):
            token['comment'] = 'Duplicate of ' + next(dup[1] for dup in duplicates if dup[0] == token['name'])
        updated_tokens_list.append(token)

    return updated_tokens_list, duplicates

# URL of the JSON data
json_url = 'https://static.optimism.io/optimism.tokenlist.json'

# Naming scheme for the output files based on chainId
output_file_names = {
    1: 'ethereum.json',
    10: 'optimism.json',
    8453: 'base.json',
    5: 'goerli.json',
    84531: 'base-goerli.json',
    420: 'optimism-goerli.json',
    424: 'public-goods-network.json',
    11155111: 'ethereum-sepolia.json',
    11155420: 'optimism-sepolia.json'
}

# Run the script on your local machine to process the files
fetch_and_process_json(json_url, output_file_names)

