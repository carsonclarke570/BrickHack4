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
# Gets the list of setlist from a search query
#
# Params:
#   artist: the artist who performed on the tour
#   date: the date of the concert
#   venue: the venue name
#   city: the city name
#   page: page number of results
#
# Returns:
#   A list of setlist based on the search parameters
#
def get_data_by_search(artist, date, venue, city, page):
    artist = "artistName=" + urllib.quote(artist.encode('utf8')) + "&"
    if artist == "artistName=&":
        artist = ""

    date = ymd_to_dmy(date)
    date = "date=" + urllib.quote(date.encode('utf8')) + "&"
    if date == "date=--&":
        date = ""

    venue = "venueName=" + urllib.quote(venue.encode('utf8')) + "&"
    if venue == "venueName=&":
        venue = ""

    city = "cityName=" + urllib.quote(city.encode('utf8')) + "&"
    if city == "cityName=&":
        city = ""

    url = "https://api.setlist.fm/rest/1.0/search/setlists?" + artist + city + venue + date + "p=" + str(page)
    data = json.loads(requests.get(url, headers=HEADERS).text)
    pprint.pprint(data)

    if 'code' in data.keys() and data['code'] == 404:
        return None

    return data['setlist']

#
# Gets the list of songs played on a specific tour
#
# Params:
#   artist: the artist who performed on the tour
#   tour: the name of the tour
#
# Returns:
#   A list of songs played by artist on their tour or
#   None if no search results could be found
#
def get_data_by_tour(artist, tour):
    artist = urllib.quote(artist.encode('utf8'))
    tour = urllib.quote(tour.encode('utf8'))
    url = "https://api.setlist.fm/rest/1.0/search/setlists?artistName=" + artist + "&tourName=" + tour + "&"
    data = json.loads(requests.get(url, headers=HEADERS).text)

    if 'code' in data.keys() and data['code'] == 404:
        return None

    songs = []
    for lst in data['setlist']:
        for set in lst['sets']['set']:
            for song in set['song']:
                if not song['name'] in songs:
                    songs.append(song['name'])

    return {"songs" : songs, "artist": data['setlist'][0]['artist']['name'], "tour": data['setlist'][0]['tour']['name']}

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
#   or None if no search results could be found
#
def get_songs_by_event(artist, date):
    artist = urllib.quote(artist.encode('utf8'))
    date = ymd_to_dmy(date)
    date = urllib.quote(date.encode('utf8'))
    r = requests.get("https://api.setlist.fm/rest/1.0/search/setlists?date=" + date + "&artistName=" + artist, headers=HEADERS)
    data = json.loads(r.text)

    if 'code' in data.keys() and data['code'] == 404:
        return None

    songs = []
    for set in data['setlist'][0]['sets']['set']:
        for song in set['song']:
            songs.append(song['name'])
    return {"songs" : songs, "artist": data['setlist'][0]['artist']['name'], "tour": data['setlist'][0]['tour']['name']}

#
# Converts a date string from yyyy-mm-dd to dd-mm-yy
#
# Params:
#   date: the date to convert
#
# Returns:
#   Converted date
#
def ymd_to_dmy(date):
    return date[8:10] + "-" + date[5:7] + "-" + date[0:4]