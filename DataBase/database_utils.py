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
        return result[0]["public_key"]
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    
def add_transaction(user1: str, user1_public_key: str, user2: str, user2_public_key: str, data: str): 
    """
    Adds a transaction between two users to the database.
    Args:
        user1 (str): The identifier for the first user.
        user1_public_key (str): The public key of the first user.
        user2 (str): The identifier for the second user.
        user2_public_key (str): The public key of the second user.
        data (str): The data associated with the transaction.
    Raises:
        Exception: If the server returns an error status code.
    Returns:
        None
    """

    current_time = datetime.now(pytz.utc).isoformat()

    key1 = user1_public_key.encode("utf-8")
    key2 = user2_public_key.encode("utf-8")

    # New transaction instance created
    transaction = Transaction(user1, user2, None, None, None, None, data, current_time)

    # The transaction datas are encrypted
    enc_transaction =  encrypt_rsa_transaction(key1 , key2, transaction)

    # Sending request to add the transaction to the database
    response = requests.post(transaction_url, headers=headers, json=enc_transaction.to_dict())

    # Verify the success of the operation
    if response.status_code == 201:  
        print("Transaction completed successfully")
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")

def get_transactions(user: str) -> list[Transaction]:
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

            # For every row a new transaction instance is created
            encrypted_transaction = Transaction(
                user1 = item['user1'],
                user2 = item['user2'],
                enc_data=item['enc_data'],
                user1_aes_key=item['user1_AES_encrypted_key'],
                user2_aes_key=item['user2_AES_encrypted_key'],
                aes_nounce=item['iv'],
                tag=item['tag'],
                created_at = item['created_at']
            )

            transactions.append(encrypted_transaction)
        return transactions
    
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    
def add_user_row(user_data):
    """
    Adds a new user row to the database.
    This function sends a POST request to the specified user URL with the provided user data.
    If the request is successful (status code 201), it prints a success message.
    Otherwise, it raises an exception with the server error details.
    Args:
        user_data (dict): A dictionary containing the user data to be added.
    Raises:
        Exception: If the server returns an error status code, an exception is raised with the error details.
    """
    
    response = requests.post(user_url, headers=headers, json=user_data)

    if response.status_code == 201:  # 201 indicates that the creation was successful
        print("New row added successfully")
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    
def add_certificate(user: str, cert_path: str):
    """
    Adds a certificate for a user to the database.
    Args:
        user (str): The identifier for the user.
        cert_path (str): The path to the certificate file.
    Raises:
        Exception: If the server returns an error status code.
    Returns:
        None
    """
    with open(cert_path, "r") as cert_file:
        certificate = cert_file.read()

    data = {
        "email": user,
        "certificate": certificate
    }

    url_with_filter = f"{user_url}?email=eq.{user}"

    response = requests.post(url_with_filter, headers=headers, json=data)

    if response.status_code == 204:
        print("Certificate added successfully")
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    