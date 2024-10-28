import requests
import pytz
from datetime import datetime
from Cryptography.cryptography_utils import text_hash, equals, get_mac_address
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
        "select": "password, secret_code",
        "email": f"eq.{usr}",
    }
    response = requests.get(user_url, headers=headers, params=data)
    if response.status_code == 200:
        result = response.json()
        if result:
            return result[0]["password"], result[0]["secret_code"]
    return None

def user_login(usr: str, psw: str, secret_code: str):
    if psw == "" and secret_code == "": 
        data = {
        "select": "email, touch_id, touch_id_device",
        "email": f"eq.{usr}",
        }

        response = requests.get(user_url, headers=headers, params=data)

        if response.status_code == 200:
            result = response.json()
            result = result[0]
            if result and result["touch_id"] == True and result["touch_id_device"] == get_mac_address():
                if authenticate(): 
                    return get_user_data(usr)
            else: 
                raise Exception("Touch ID not enabled or not available on this device")
            
        else:
            raise Exception("Server error")
    else: 

        hashed_psw, hashed_secret_code = get_hashed(usr)
        if equals(psw, hashed_psw) and equals(secret_code, hashed_secret_code):
            return get_user_data(usr)



def get_user_data(usr):
    data = {
        "select": "email, name, surname, money, birthday, last_balance_update, touch_id, touch_id_device",
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
    
def add_transaction(user1: str, user2: str, amount: int, description: str): 
    current_time = datetime.now(pytz.utc).isoformat()

    data = {
        "user1": user1,
        "created_at": current_time,
        "user2": user2,
        "money": amount,
        "description": description,
        "AES_key": "AES",
        "iv": "iv"
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
        "select": "user1, created_at, user2, money, description",
        "or": f"(user1.eq.{user},user2.eq.{user})",
        "order": "created_at.asc"
    }

    response = requests.get(transaction_url, headers=headers, params=data)
    print(response)

    # Verifica il successo dell'operazione
    if response.status_code == 200:  # 204 indica che l'aggiornamento è avvenuto con successo, ma senza risposta nel corpo
        result = response.json()
        return result
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
    