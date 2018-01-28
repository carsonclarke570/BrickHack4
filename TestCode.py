#
# Copyright (C) Carson Clarke-Magrab/Eric Kanis - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Carson Clarke-Magrab <ctc7359@rit.edu> & Eric Kanis <erk2974@rit.edu>, January 2018
#
# Spotify_Midware.py
#
# Interacts with Spotify
#

import json
from flask import Flask, request, redirect, render_template
import requests
import base64
import Util
import sys
import Setlist_Scraper
import pprint

app = Flask(__name__)

#Spotify stuff
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Client keys
CLIENT_ID = "5dad0a666d5d4b8c948dddb2bd0b289e"
CLIENT_SECRET = "6fb2226430624c34961363a8264e6bf8"

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

AUTH_QUERY = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

#Test code
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}


@app.route("/")
def index():
    auth_url = Util.make_url_args(SPOTIFY_AUTH_URL, auth_query_parameters)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    auth_header_json = {"Authorization": "Bearer {}".format(access_token), "Content-Type": "application/json"}

    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=auth_header)
    user_id = json.loads(profile_response.text)["id"]

    option = sys.argv[1]
    print sys.argv
    search_args = sys.argv[2:]
    songs = {}
    artist = None
    title = ""
    if option == "-t":
        artist = search_args[0]
        tour_name = search_args[1]
        title = artist + " during " + tour_name
        songs = Setlist_Scraper.get_songs_by_tour(artist, tour_name)

    if option == "-c":
        artist = search_args[0]
        date = search_args[1]
        venue = search_args[2]
        title = artist + " at " + venue + " on " + date
        songs = Setlist_Scraper.get_songs_by_event(artist, date, venue)

    song_ids = []
    for i in songs:
        response = Util.get_song(artist, i, auth_header)
        song_ids.append("spotify:track:" + response["id"])

    print song_ids
    playlist_id = Util.init_playlist(user_id, title, auth_header_json)["id"]
    Util.add_song(song_ids, user_id, playlist_id, auth_header_json)

    #stuff = Util.init_playlist(user_id, "Test", auth_header_json)
    #stuff = Util.add_song({"4iV5W9uYEdYUVa79Axb7Rh"}, user_id, stuff["id"], auth_header_json)

    # Combine profile and playlist data to display
    display_arr = {}
    return render_template("index.html", sorted_array=display_arr)


if __name__ == "__main__":
    app.run(debug=True, port=PORT)