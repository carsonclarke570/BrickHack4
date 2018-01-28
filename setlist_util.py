#
# Copyright (C) Carson Clarke-Magrab/Eric Kanis - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Carson Clarke-Magrab <ctc7359@rit.edu> & Eric Kanis <erk2974@rit.edu>, January 2018
#

#
# File: setlist_util.py
# Date: 1/27/2018
# Authors: Eric Kanis
# Description: Provides helper functions to scrape data from Setlist.fm
#


import json, math, pprint, requests, urllib

# headers for GET requests
HEADERS = {"Accept": "application/json", "x-api-key": "7a66baa8-d27c-4718-88ec-5f55d285b643"}
ITEMS_PER_PAGE = 20

#
# Gets the list of songs played on a specific tour
#
# Params:
#   artist: the artist who perfromed the tour
#   tour: the name of the tour
#
# Returns:
#   A list of songs played by artist on their tour
#
def get_songs_by_tour(artist, tour):
    artist = urllib.quote(artist.encode('utf8'))
    tour = urllib.quote(tour.encode('utf8'))
    url = "https://api.setlist.fm/rest/1.0/search/setlists?artistName=" + artist + "&tourName=" + tour
    r = requests.get(url, headers=HEADERS)
    data = json.loads(r.text)
    numPages = int(math.ceil(float(data['total'])/ITEMS_PER_PAGE))
    songs = []
    for page in range(1, numPages+1):
        r = requests.get(url + "&p=" + str(page), headers=HEADERS)
        setlists = r.json()['setlist']
        for lst in setlists:
            for set in lst['sets']['set']:
                for song in set['song']:
                    if not song['name'] in songs:
                        songs.append(song['name'])
    return songs

#
# Gets the list of songs played on a specific concert date
#
# Params:
#   artist: the artist who performed the concert
#   date: the date of the concert
#   venue: the venue of the concert
#
# Returns:
#   A list of songs played by artist at a specific concert
#
def get_songs_by_event(artist, date, venue):
    artist = urllib.quote(artist.encode('utf8'))
    date = urllib.quote(date.encode('utf8'))
    venue = urllib.quote(venue.encode('utf8'))
    r = requests.get("https://api.setlist.fm/rest/1.0/search/setlists?date=" + date + "&artistName=" + artist + "&venueName=" + venue, headers=HEADERS)
    data = json.loads(r.text)

    pprint.pprint(data)
    songs = []
    for set in data['setlist'][0]['sets']['set']:
        for song in set['song']:
            songs.append(song['name'])
    return songs

