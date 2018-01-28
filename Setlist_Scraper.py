#
# Copyright (C) Carson Clarke-Magrab/Eric Kanis - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Carson Clarke-Magrab <ctc7359@rit.edu> & Eric Kanis <erk2974@rit.edu>, January 2018
#
# Setlist_Scraper.y
#
# Collects setlist information from setlist.fm
#

import requests
import json
import pprint

headers = { "Accept" : "application/json", "x-api-key" : "a13409ea-3590-4eca-ac71-d013db6e9d1b"}
r = requests.get('https://api.setlist.fm/rest/1.0/search/venues?cityName=Chicago&p=1', headers=headers)
js = r.json()

pprint.pprint(js)