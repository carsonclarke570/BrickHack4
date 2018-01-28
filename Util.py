#
# Copyright (C) Carson Clarke-Magrab/Eric Kanis - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Carson Clarke-Magrab <ctc7359@rit.edu> & Eric Kanis <erk2974@rit.edu>, January 2018
#

import urllib
import requests
import json

# URL Constants
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

# Spotify requests

def add_song(song_uris, user_id, playlist_id, auth):
    add_song_endpoint = "{}/users/{}/playlists/{}/tracks".format(SPOTIFY_API_BASE_URL, user_id, playlist_id)
    print add_song_endpoint
    add_song_response = requests.post(add_song_endpoint, data=json.dumps({"uris": song_uris}), headers=auth)
    print add_song_response
    return json.loads(add_song_response.text)

def init_playlist(user_id, name, auth):
    create_plist_endpoint = "{}/users/{}/playlists".format(SPOTIFY_API_BASE_URL, user_id)
    create_plist_endpoint = requests.post(create_plist_endpoint, data="{\"name\":\"" + name + "\", \"public\":false}", headers=auth)
    return json.loads(create_plist_endpoint.text)

def get_song(artist, song, auth):
    song_api_endpoint = "{}/search".format(SPOTIFY_API_BASE_URL);
    res = song_api_endpoint + "?q=" + urllib.quote(song) + "+" + urllib.quote(artist)
    res = res + "&type=track&limit=1";
    song_api_response = requests.get(res, headers=auth)
    song_api_response = json.loads(song_api_response.text)
    for i in song_api_response["tracks"]["items"]:
        for j in i["artists"]:
            if j["name"].lower() == artist.lower():
                song_api_response = i

    return song_api_response

# Misc utilities


def make_url_args(url, params):
    url_args = "&".join(["{}={}".format(key, urllib.quote(val)) for key, val in params.iteritems()])
    return "{}/?{}".format(url, url_args)

