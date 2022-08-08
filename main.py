import base64, requests
from turtle import end_poly
from unittest.mock import seal
import datetime
from auth import client_id, client_secret
from urllib.parse import urlencode

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
            raise Exception("could not authenticate client.")
            return False
        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now 
        return True

    def get_access_token(self):
        auth_done = self.perform_auth()
        if not auth_done:
            raise Exception("Not Authorized..")
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
    
    def get_resource_headers(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization" : f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type='albums', version="v1"):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_headers()
        r = requests.get(endpoint, headers=headers)
        print(r.status_code, "\n", endpoint)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')
    
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def base_search(self, query_params):
        headers = self.get_resource_headers()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        print("search status..",r.status_code)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query == None:
            raise Exception("Empty query. Query reqrd..")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
            print(query)
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator.upper()
                if isinstance(operator, str):
                    query = f"{query} {operator} {operator_query}"
        query_params =urlencode({'q': query, "type":search_type.lower()})
        return self.base_search(query_params)

import json
def cred():
    return client_id, client_secret

client = SpotifyApi(client_id, client_secret)
client.perform_auth()
print(client.access_token)
# response = client.search("Moon", search_type="track")['tracks']['items']
# for i in response:
#     print(i, "\n \n")
# print(response[1]['album'])


# print(client.get_artist('0du5cEVh5yTK9QJze8zA0C')['name'])
# print(client.search({"track":"moon", "artist":"Kanye West"}, search_type="track"))
print(client.search(query={"track":"Hostage"},operator='NOT', operator_query='sia', search_type="track")['tracks']['items'])