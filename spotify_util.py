#
# Copyright (C) Carson Clarke-Magrab/Eric Kanis - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Carson Clarke-Magrab <ctc7359@rit.edu> & Eric Kanis <erk2974@rit.edu>, January 2018
#

#
# File: spotify_util.py
# Date: 1/27/2018
# Authors: Carson Clarke-Magrab
# Description: Provides helper functions to interact with Spotify
#

import json, requests, urllib

# URL Constants
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

#
# Adds a set of songs to a specific playlist
#
# Params:
#   song_uris: a list of the Spotify URIs of songs to add
#   user_id: the Spotify id of the user who owns the playlist
#   playlist_id: the Spotify id of the playlist to add to
#   auth: the authorization header
#
# Returns:
#   The response JSON
#
def add_song(song_uris, user_id, playlist_id, auth):
    add_song_endpoint = "{}/users/{}/playlists/{}/tracks".format(SPOTIFY_API_BASE_URL, user_id, playlist_id)
    print add_song_endpoint
    add_song_response = requests.post(add_song_endpoint, data=json.dumps({"uris": song_uris}), headers=auth)
    print add_song_response
    return json.loads(add_song_response.text)

#
# Creates a new playlist
#
# Params:
#   user_id: the Spotify id of the user to create a playlist for
#   name: name of the playlist
#   auth: the authorization header
#
# Returns:
#   The response JSON
#
def init_playlist(user_id, name, auth):
    create_plist_endpoint = "{}/users/{}/playlists".format(SPOTIFY_API_BASE_URL, user_id)
    create_plist_endpoint = requests.post(create_plist_endpoint, data="{\"name\":\"" + name + "\", \"public\":false}", headers=auth)
    return json.loads(create_plist_endpoint.text)

#
# Gets the Spotify JSON associated with a specific song
#
# Params:
#   artists: the name of the artist
#   song: the name of the song
#   auth: the authourization header
#
# Returns:
#   The response JSON
#
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



