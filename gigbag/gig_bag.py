#
# Copyright (C) Carson Clarke-Magrab/Eric Kanis - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Carson Clarke-Magrab <ctc7359@rit.edu> & Eric Kanis <erk2974@rit.edu>, January 2018
#

#
# File: gig_bag.py
# Date: 1/27/2018
# Authors: Eric Kanis & Carson Clarke-Magrab
# Description: The GigBag app coverts set lists from various tours and concerts into Spotify playlists
#
#       Usage: gig_bag -flags [artist] <flag dependent arguments>
#       1)     gig_bag -c [artist] [date] [venue]
#           artist: artist's name
#           date: date of specific concert (Format: [day]-[month]-[year])
#`          venue: name of venue
#       2)     gig_bag -t [artist] [tour]
#           artist: artist's name
#           tour: name of tour
#

import base64, json, os, requests, sys, urllib

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gigbag.lib import spotify_util, setlist_util
from flask import Flask, request, redirect, render_template

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

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID,
    "state": ""
}

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

#
# Redirects to Spotify's authorization service
#
# Returns:
#    A redirect to the Spotify authorization service
#
@app.route("/authorize", methods=['GET', 'POST'])
def authorize():
    artist = request.args.get('artist')
    tour = request.args.get('tour')
    state_json = json.dumps({"artist": artist, "tour": tour})
    auth_query_parameters['state'] = state_json
    url_args = "&".join(["{}={}".format(key, urllib.quote(val)) for key, val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

#
# Confirms Spotify authorization and creates playlist from commandline data
#
# Returns:
#   Renders index.html
#
@app.route("/callback/q", methods=['GET', 'POST'])
def callback():
    data = json.loads(request.args.get('state'))
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

    # authorization headers
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    auth_header_json = {"Authorization": "Bearer {}".format(access_token), "Content-Type": "application/json"}

    # get user info
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=auth_header)
    user_id = json.loads(profile_response.text)["id"]

    # Get data from URL
    artist = data['artist']
    tour_name = data['tour']

    # Get data from setlist.fm
    setlist_data = setlist_util.get_data_by_tour(artist, tour_name);
    songs = setlist_data['songs']
    artist = setlist_data['artist']
    tour_name = setlist_data['tour']
    title = artist + "[" + tour_name + "]"



    # if option == "-c":
    #     artist = search_args[0]
    #     date = search_args[1]
    #     venue = search_args[2]
    #     title = artist + " at " + venue + " on " + date
    #     songs = setlist_util.get_songs_by_event(artist, date, venue)

    context = []
    song_ids = []
    for i in songs:
        response = spotify_util.get_song(artist, i, auth_header)
        if 'id' in response.keys():
            s_id = "spotify:track:" + response["id"]
            a_url = response["album"]["images"][2]["url"]
            context.append({"s_name": i, "a_url": a_url})
            song_ids.append(s_id)
        else:
            songs.remove(i)


    # create Spotify playlist
    playlist_id = spotify_util.init_playlist(user_id, title, auth_header_json)["id"]

    # add songs to playlist
    spotify_util.add_song(song_ids, user_id, playlist_id, auth_header_json)

    return render_template("success.html", context=context)

if __name__ == '__main__':
    app.run(debug=True, port=PORT)