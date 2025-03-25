CLIENT_ID = "aYapqR9xCYjqHgkK"
CLIENT_SECRET = "xhPw0matROH6ZeuvLbYX6taV1jEpj0HaQddO4pn60EQ="

import requests
import webbrowser
import base64
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# 🔹 Step 1: OAuth Configuration
# CLIENT_ID = "<YOUR_CLIENT_ID>"
# CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"
REDIRECT_URI = "http://localhost:9090/callback"
AUTH_URL = "https://login.tidal.com/oauth2/authorize"
TOKEN_URL = "https://auth.tidal.com/v1/oauth2/token"
API_BASE_URL = "https://api.tidal.com/v1"

# Storage for auth code
auth_code = None


# 🔹 Step 2: Handle Redirect and Capture Authorization Code
class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        if "code=" in self.path:
            auth_code = self.path.split("code=")[1].split("&")[0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()


# Start a temporary HTTP server to capture the authorization code
def start_server():
    server = HTTPServer(("localhost", 9090), AuthHandler)
    server.handle_request()


# 🔹 Step 3: Get Authorization Code
def get_auth_code():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "r_usr",
    }
    auth_request_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    print(f"🔗 Open this URL to authenticate: {auth_request_url}")
    webbrowser.open(auth_request_url)

    # Start a temporary HTTP server to listen for the response
    start_server()
    return auth_code


# 🔹 Step 4: Exchange Authorization Code for Access Token
def get_access_token(auth_code):
    if not auth_code:
        print("❌ No authorization code received!")
        return None

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {"Authorization": f"Basic {b64_credentials}"}
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"✅ Access token retrieved: {token}")
        return token
    else:
        print("❌ Error getting access token:", response.text)
        return None


# 🔹 Step 5: Get User ID
def get_user_id(access_token):
    if not access_token:
        print("❌ No access token available!")
        return None

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{API_BASE_URL}/users/me", headers=headers)

    if response.status_code == 200:
        return response.json()["userId"]
    else:
        print("❌ Error fetching user ID:", response.text)
        return None


# 🔹 Step 6: Fetch User Playlists
def get_playlists(access_token, user_id):
    if not access_token:
        print("❌ No access token available!")
        return []

    url = f"{API_BASE_URL}/users/{user_id}/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print("❌ Error fetching playlists:", response.text)
        return []


# 🔹 Step 7: Fetch Tracks from a Playlist
def get_playlist_tracks(access_token, playlist_id):
    if not access_token:
        print("❌ No access token available!")
        return []

    url = f"{API_BASE_URL}/playlists/{playlist_id}/items"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print("❌ Error fetching tracks:", response.text)
        return []


# 🔹 Run the Authentication & Fetch Playlists
auth_code = get_auth_code()
access_token = get_access_token(auth_code)

if access_token:
    user_id = get_user_id(access_token)

    if user_id:
        playlists = get_playlists(access_token, user_id)

        if playlists:
            print("\n🎵 Your Playlists:")
            for idx, playlist in enumerate(playlists):
                print(f"{idx + 1}. {playlist['title']} (ID: {playlist['uuid']})")

            # Select a playlist
            selected_idx = int(input("\nEnter the number of the playlist to view tracks: ")) - 1
            playlist_id = playlists[selected_idx]["uuid"]

            # Fetch and Display Tracks
            tracks = get_playlist_tracks(access_token, playlist_id)

            print("\n🎶 Tracks in Playlist:")
            for idx, track in enumerate(tracks):
                track_info = track["item"]
                print(f"{idx + 1}. {track_info['title']} - {track_info['artist']['name']}")

