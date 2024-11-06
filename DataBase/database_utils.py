import requests
import pytz
import ast
from datetime import datetime
from Cryptography.cryptography_utils import *
from Cryptography.touchid import authenticate


user_url = "https://ipjvdwudqwizxnxjfzyx.supabase.co/rest/v1/user"
transaction_url = "https://ipjvdwudqwizxnxjfzyx.supabase.co/rest/v1/transaction"

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwanZkd3VkcXdpenhueGpmenl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzOTE5MzEsImV4cCI6MjA0Mzk2NzkzMX0.hBIDK3PzXBHYAWmVPg3M0NbX19jXHRwow3BEyt_juIM"

# Headers della richiesta
headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_hashed(usr: str):
    """
    Retrieves the hashed password and secret code for a given user from the database.
    Args:
        usr (str): The email of the user whose hashed password and secret code are to be retrieved.
    Returns:
        tuple: A tuple containing the hashed password and secret code if the user is found, otherwise None.
    """

    data = {
        "select": "password, salt",
        "email": f"eq.{usr}",
    }
    response = requests.get(user_url, headers=headers, params=data)
    if response.status_code == 200:
        result = response.json()
        if result:
            return result[0]["password"], result[0]["salt"]
    return None



def get_user_data(usr):
    data = {
        "select": "*",
        "email": f"eq.{usr}",
    }

    response = requests.get(user_url, headers=headers, params=data)

    print(response)

    if response.status_code == 200:
        result = response.json()
        if result:
            return result[0]
    else:
        raise Exception("Server error")

def update_touch_id(usr: str, touch_id: bool, touch_id_device: str):
    # Data to be updated
    data = {
        "email": usr,
        "touch_id": touch_id,
        "touch_id_device": touch_id_device
    }

    # URL specified with the filter
    url_with_filter = f"{user_url}?email=eq.{usr}"

    # execute the PATCH request
    response = requests.patch(url_with_filter, headers=headers, json=data)
    print(response)

    # Verify the success of the operation
    if response.status_code == 204:  # 204 indicates that the update was successful, but without a response in the body
        print("Database updated successfully")
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    
def upadate_balance(usr: str, amount: int):
    # Data to be updated
    data = {
        "money": amount,
        "last_balance_update": datetime.now(pytz.utc).isoformat()
    }

    # URL specified with the filter
    url_with_filter = f"{user_url}?email=eq.{usr}"

    # execute the PATCH request
    response = requests.patch(url_with_filter, headers=headers, json=data)
    print(response)

    # Verify the success of the operation
    if response.status_code == 204:  # 204 indicates that the update was successful, but without a response in the body
        print("Database updated successfully")
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    
def get_user_public_key(user: str): 
    data = {
        "select": "public_key",
        "email": f"eq.{user}",
    }

    response = requests.get(user_url, headers=headers, params=data)
        # Verifica il successo dell'operazione
    if response.status_code == 200:  # 204 indica che l'aggiornamento è avvenuto con successo, ma senza risposta nel corpo
        
        result = response.json()
        return result[0]
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    
def add_transaction(user1: str, user1_public_key: str, user2: str, user2_public_key: str, data: str): 
    current_time = datetime.now(pytz.utc).isoformat()

    key1 = ast.literal_eval(user1_public_key)
    key2 = ast.literal_eval(user2_public_key)

    encrypted_data =  encrypt_rsa_transaction(ast.literal_eval(user1_public_key), ast.literal_eval(user2_public_key), data)

    data = {
        "user1": user1,
        "created_at": current_time,
        "user2": user2,
        "enc_data": str(encrypted_data.cyphertext),
        "user1_AES_encrypted_key": str(encrypted_data.user1_aes_key),
        "user2_AES_encrypted_key": str(encrypted_data.user2_aes_key),
        "iv": str(encrypted_data.aes_nounce),
        "tag": str(encrypted_data.tag)
    }

    response = requests.post(transaction_url, headers=headers, json=data)
    print(response)

    # Verifica il successo dell'operazione
    if response.status_code == 201:  # 201 indica che la creazione è avvenuta con successo
        print("Transaction completed successfully")
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")

def get_transactions(user: str):
    data = {
        "select": "*",
        "or": f"(user1.eq.{user},user2.eq.{user})",
        "order": "created_at.asc"
    }

    response = requests.get(transaction_url, headers=headers, params=data)

    if response.status_code == 200:
        result = response.json()
        transactions = []
        for item in result:
            encrypted_transaction = EncryptedTransaction(
                cyphertext=item['enc_data'],
                user1_aes_key=item['user1_AES_encrypted_key'],
                user2_aes_key=item['user2_AES_encrypted_key'],
                aes_nounce=item['iv'],
                tag=item['tag']
            )
            transactions.append({
                'id': item['id'],
                'created_at': item['created_at'],
                'user1': item['user1'],
                'user2': item['user2'],
                'encrypted_transaction': encrypted_transaction
            })
        return transactions
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    
def new_row(user_data):
    
    response = requests.post(user_url, headers=headers, json=user_data)

    if response.status_code == 201:  # 201 indicates that the creation was successful
        print("New row added successfully")
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    