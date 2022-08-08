import base64, requests
import datetime
from auth import client_id, client_secret


class SpotifyApi(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret

        if client_id == None or client_secret == None:
            raise Exception("client credentials not set.")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64f = base64.b64encode(client_creds.encode())
        return client_creds_b64f.decode()

    def get_token_headers(self):
        client_creds_b64f = self.get_client_credentials()
        return {
            'Authorization': f'Basic {client_creds_b64f}'
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        
        r = requests.post(token_url, data=token_data, headers=token_headers)
        # print(r.json(), "\n", r.status_code)
        data = r.json()
        if r.status_code not in range(200, 299):
            return False
        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires_in
        self.access_token_did_expire = expires < now 
        return True

def cred():
    return client_id, client_secret

client = SpotifyApi(client_id, client_secret)
client.perform_auth()
print(client.access_token)
        