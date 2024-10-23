import requests

from Cryptography.cryptography_utils import password_hash, password_check

url = "https://ipjvdwudqwizxnxjfzyx.supabase.co/rest/v1/user"

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwanZkd3VkcXdpenhueGpmenl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzOTE5MzEsImV4cCI6MjA0Mzk2NzkzMX0.hBIDK3PzXBHYAWmVPg3M0NbX19jXHRwow3BEyt_juIM"

# Headers della richiesta
headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_hashed_pwd(usr: str):
    data = {
        "select": "password",
        "email": f"eq.{usr}",
    }
    response = requests.get(url, headers=headers, params=data)
    if response.status_code == 200:
        result = response.json()
        if result:
            return result[0]["password"]
    return None

def user_login(usr: str, psw: str):
    if password_check(psw, get_hashed_pwd(usr)):
        data = {
            "select": "email, name, surname, money, birthday",
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

    return None
