import base64, requests, datetime


client_id = '3d7492....024d239'
client_secret = '67d182ae.....6fdaf4e7'

client_creds = f"{client_id}:{client_secret}"

client_creds_b64f = base64.b64encode(client_creds.encode())
# print(client_creds_b64f.decode())


# we have to grab our token
token_url = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = {
    "grant_type": 'client_credentials'
}
token_headers = {'Authorization': f'Basic {client_creds_b64f.decode()}'}

r = requests.post(token_url, data=token_data, headers=token_headers)
# print(r.json(), "\n", r.status_code)
valid_request = r.status_code in range(200, 299)

token_response_data = r.json()

if valid_request:
    now = datetime.datetime.now()
    access_token = token_response_data["access_token"]
    expires_in = token_response_data["expires_in"]
    expires = now + datetime.timedelta(seconds=expires_in)
    did_expire = expires < now
