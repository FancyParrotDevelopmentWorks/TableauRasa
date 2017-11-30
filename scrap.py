# This example shows how to use the Tableau Server REST API
# to sign in to a server, get back an authentication token and
# site ID, and then sign out.
# The example runs in Python 2.7 and Python 3.3 code


import requests
import json
import os


HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json'
}

TOKEN = None
SITE_ID = None

def update_headers(key, value):
    global HEADERS
    HEADERS[key] = value

def signin(server_url, user_name, password, headers, site_url_id=""):

    signin_url = "{server_url}/api/2.5/auth/signin".format(server_url=server_url)
    payload = {"credentials": {"name": user_name, "password": password , "site": {"contentUrl": site_url_id}}}

    req = requests.post(signin_url, json=payload, headers=headers)
    req.raise_for_status()
    response = json.loads(req.content)

    # Get the authentication token from the <credentials> element
    token = response["credentials"]["token"]

    # Get the site ID from the <site> element
    site_id = response["credentials"]["site"]["id"]

    print('Sign in successful!')
    print('\tToken: {token}'.format(token=token))
    print('\tSite ID: {site_id}'.format(site_id=site_id))
    print(response)

    return token, site_id

data = json.load(open('private_creds.json', 'rb'))

#TOKEN, SITE_ID = signin(server_name=server_name, user_name=data['un'], password=data['pw'], site_url_id=site_url_id)
# Set the authentication header using the token returned by the Sign In method.
#

# ... Make other calls here ...

def download_image(token, img_url, destination_path):
    resp = requests.get(img_url, cookies = {'workgroup_session_id': token})
    resp.raise_for_status() #throws error if status code != 200

    with open(destination_path, 'wb') as f:
        f.write(resp.content)
        print('Downloaded {img} to {path}'.format(img = img_url, path = destination_path))

def signout(server_url, headers):
    # Sign out
    signout_url = "{server_url}/api/2.5/auth/signout".format(server_url=server_url)
    req = requests.post(signout_url, data=b'', headers=headers)
    req.raise_for_status()
    print('Sign out successful!')

if __name__ == "__main__":
    import time

    CREDS = json.load(open('private_creds.json', 'rb'))


    SERVER_NAME = CREDS['server']  # Name or IP address of your installation of Tableau Server
    USERNAME = CREDS['un']
    PASSWORD = CREDS['pw']
    SITE_URL = 'Default'

    cwd = os.getcwd()
    images_dir = os.path.join(cwd, 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)




    #sign in
    token, site_id = signin(server_url=SERVER_NAME, user_name=USERNAME, password=PASSWORD, site_url_id=SITE_URL, headers=HEADERS)
    # Set the authentication header using the token returned by the Sign In method.
    update_headers('X-tableau-auth', token)


    path = os.path.join(images_dir, 'img_%d.jpeg'%int(time.time()))

    download_image(token = token, img_url=CREDS['test_img_url'], destination_path=path)

    signout(server_url=SERVER_NAME, headers = HEADERS)

