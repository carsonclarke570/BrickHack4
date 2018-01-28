#
# Copyright (C) Carson Clarke-Magrab/Eric Kanis - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Carson Clarke-Magrab <ctc7359@rit.edu> & Eric Kanis <erk2974@rit.edu>, January 2018
#
# Setlist_Scraper.py
#
# Collects setlist information from setlist.fm
#

import sys
import requests
import pprint
import urllib
import math

headers = {"Accept": "application/json", "x-api-key": "7a66baa8-d27c-4718-88ec-5f55d285b643"}

def getargs(argv):
    args = {}
    while argv:
        if argv[0][0] == '-':
            args[argv[0]] = argv[1]
        argv = argv[1:]
    return args

def get_songs_by_tour(artist, tour):
    artist = urllib.quote(artist)
    tour = urllib.quote(tour)
    url = "https://api.setlist.fm/rest/1.0/search/setlists?artistName=" + artist + "&tourName=" + tour
    r = requests.get(url, headers=headers)
    data = r.json()
    numPages = int(math.ceil(data['total']/20))
    songs = []
    for page in range(1, numPages+1):
        r = requests.get(url + "&p=" + str(page), headers=headers)
        setlists = r.json()['setlist']
        for lst in setlists:
            for set in lst['sets']['set']:
                for song in set['song']:
                    if not song['name'] in songs:
                        songs.append(song['name'])
    return songs




    pprint.pprint(r.json())
    return songs

def get_songs_by_event(artist, date, venue):
    artist = urllib.quote(artist)
    date = urllib.quote(date)
    venue = urllib.quote(venue)
    r = requests.get("https://api.setlist.fm/rest/1.0/search/setlists?date=" + date + "&artistName=" + artist + "&venueName=" + venue, headers=headers)
    data = r.json()

    pprint.pprint(data)
    songs = data['setlist'][0]['sets']['set'][0]['song']
    return songs


def main():

    option = sys.argv[1]
    print sys.argv
    search_args = sys.argv[2:]
    songs = {}
    if option == "-t":
        artist = search_args[0]
        tour_name = search_args[1]
        songs = get_songs_by_tour(artist, tour_name)
        for song in songs:
            print song + '\n'

    if option == "-c":
        artist = search_args[0]
        date = search_args[1]
        venue = search_args[2]
        songs = get_songs_by_event(artist, date, venue)

main()
