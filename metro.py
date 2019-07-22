#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      MaanuelMM
# Credits:      StackOverflow :S
# Created:      2019/07/27
# Last update:  2019/07/27

'''
The idea of this script is to obtain all available stations of 'Metro Madrid' throw their kind of API
obtained in their website. It was observed that all URLs are composed of three numbers, so we'll make
a loop from 000 to 999 to obtain which of them are valid stations:

  - If the returned list is not empty, it's supposed to be valid. (in 'k' list are the invalid ones.)
  - If the returned list is empty, it's not valid (there is no info available).
  - If there is no list (because of unauthorized petition), it's not valid too.
  - If there is no OK HTTP status, it's not valid too. In this case, it's recommended to scan all
    stations again because some error could have been happened.

Maybe it's necessary to make a sleep(x), being 'x' a number representing seconds, to avoid unexpected
errors between requests. A commented example will be provided with it's corresponding library import.

NOTE: It is possible to reduce time execution creating threads instead of making sequential requests.
'''

import requests
import json
import os
# import time

from datetime import datetime


i = 0
j = 999
v = {}  # dict of valid stations
k = []  # list of invalid formatted stations
e = []  # list of empty stations
u = []  # list of unauthorized stations
n = []  # list of non-OK HTTP status stations

while i <= j:
    szi = str(i).zfill(3)
    r = requests.get("https://www.metromadrid.es/es/metro_next_trains/modal/" + szi)
    if r.status_code == 200:
        try:
            if r.json():
                try:
                    v[r.json()[0]["dialogOptions"]["title"].split("PR\u00d3XIMOS TRENES - Estaci\u00f3n ")[1]] = szi
                except:
                    k.append(i)
            else:
                e.append(i)
        except:
            u.append(i)
    else:
        n.append(i)
    print(szi + " of " + str(j))
    i += 1
    # time.sleep(1)

print("\nValid stations:\n" + str(v) + "\n")
print("\nInvalid formatted stations:\n" + str(k) + "\n")
print("\nEmpty stations:\n" + str(e) + "\n")
print("\nUnauthorized stations:\n" + str(u) + "\n")
print("\nNon-OK HTTP stations:\n" + str(n) + "\n")

if os.path.exists('stations.json'):
    with open('stations.json', 'r', encoding='utf-8') as original_data:
        with open('stations-' + str(datetime.now()) + '.json', 'w', encoding='utf-8') as backup_data:
            json.dump(json.load(original_data), backup_data, sort_keys=True, indent=4)
    os.remove("stations.json")

with open('stations.json', 'w', encoding='utf-8') as data:
    json.dump(v, data, sort_keys=True, indent=4)
