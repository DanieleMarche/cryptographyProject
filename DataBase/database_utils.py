import requests

from Cryptography.cryptography_utils import text_hash, equals, get_mac_address
from Cryptography.touchid import authenticate


url = "https://ipjvdwudqwizxnxjfzyx.supabase.co/rest/v1/user"

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwanZkd3VkcXdpenhueGpmenl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzOTE5MzEsImV4cCI6MjA0Mzk2NzkzMX0.hBIDK3PzXBHYAWmVPg3M0NbX19jXHRwow3BEyt_juIM"

# Headers della richiesta
headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_hashed(usr: str):
    data = {
        "select": "password, secret_code",
        "email": f"eq.{usr}",
    }
    response = requests.get(url, headers=headers, params=data)
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

        response = requests.get(url, headers=headers, params=data)

        if response.status_code == 200:
            result = response.json()
            result = result[0]
            if result and result["touch_id"] == True and result["touch_id_device"] == get_mac_address():
                if authenticate(): 
                    return get_user_data(usr)
            
        else:
            raise Exception("Server error")
    else: 

        hashed_psw, hashed_secret_code = get_hashed(usr)
        if equals(psw, hashed_psw) and equals(secret_code, hashed_secret_code):
            return get_user_data(usr)



def get_user_data(usr):
    data = {
        "select": "email, name, surname, money, birthday, touch_id, touch_id_device",
        "email": f"eq.{usr}",
    }

    response = requests.get(url, headers=headers, params=data)

    print(response)

    if response.status_code == 200:
        result = response.json()
        if result:
            return result[0]
    else:
        raise Exception("Server error")

def update_database(usr: str, touch_id: bool, touch_id_device: str):
    # Dati da aggiornare
    data = {
        "touch_id": touch_id,
        "touch_id_device": touch_id_device
    }

    # URL specifico con la condizione di filtro basata sull'email
    url_with_filter = f"{url}?email=eq.{usr}"

    # Effettua la richiesta PATCH per aggiornare i dati dell'utente
    response = requests.patch(url_with_filter, headers=headers, json=data)
    print(response)

    # Verifica il successo dell'operazione
    if response.status_code == 204:  # 204 indica che l'aggiornamento è avvenuto con successo, ma senza risposta nel corpo
        print("Database updated successfully")
    else:
        raise Exception(f"Server error: {response.status_code}, {response.text}")
