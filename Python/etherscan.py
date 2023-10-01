import requests
import csv
from datetime import datetime

def convert_timestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp))

def get_token_transfers(address, api_key):
    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "sort": "desc",
        "apikey": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "1":
        transfers = data["result"]
        for transfer in transfers:
            transfer["timeStamp"] = convert_timestamp(transfer["timeStamp"])
        return transfers
    else:
        error_message = data["result"]
        raise Exception(f"API call failed: {error_message}")

# Replace 'MyApiKeyToken' with your actual API key
api_key = "7UGXIZ5DQP2UW6U2IG6DBY26QUCFMD92NT"

# Replace the example address with your desired Ethereum address
address = "0x9cbf044bc535db4c93a9f11205a69631d9dcef26"

try:
    transfers = get_token_transfers(address, api_key)
    headers = transfers[0].keys() if transfers else []
    filename = f"token_transfers_{address}.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(transfers)

    print(f"Token transfers saved to {filename}")
except Exception as e:
    print(f"Error occurred: {str(e)}")


#46HDM22T9FU5RB4S3FSAIW9N9KKJ2K7MUP