import requests
from main import client
from urllib.parse import urlencode

access_token = client.access_token
headers = {
    "Authorization" : f"Bearer {access_token}"
}
endpoint = "https://api.spotify.com/v1/search"
data =urlencode({'q': "Time", "type":"track"})

lookup_url = f"{endpoint}?{data}"
r = requests.get(lookup_url, headers=headers)
# print(r.json())
# print(r.status_code)

data2 = urlencode({'q':"Scott Mescudi", "type":"track"})
scott = f"{endpoint}?{data2}"
print(requests.get(scott, headers=headers).json())
