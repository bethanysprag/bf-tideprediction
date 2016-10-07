#!/usr/bin/env python

"""
Copyright 2016, RadiantBlue Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import glob
import csv
import sqlite3
import os
import math
from posixpath import basename

conn = sqlite3.connect("fdh.sqlite")
curs = conn.cursor()
curs.execute("""
             CREATE TABLE STATIONS \
             (id INTEGER PRIMARY KEY, \
             lat FLOAT, \
             lon FLOAT, \
             cos_lat FLOAT, \
             sin_lat FLOAT, \
             cos_lon FLOAT, \
             sin_lon FLOAT, \
             station STRING);""")

files = glob.glob("./sealevelstations.csv")

for f in files:
    try:
        reader = csv.reader(open(f, 'rU'), delimiter=',')
        for row in reader:

            try:
                station = os.path.splitext(basename(row[-1]))[0][3:]
                lat = float(row[5])
                lon = float(row[6])

                cos_lat = math.cos(lat * math.pi / 180.0)
                sin_lat = math.sin(lat * math.pi / 180.0)

                cos_lon = math.cos(lon * math.pi / 180.0)
                sin_lon = math.sin(lon * math.pi / 180.0)

                to_db = [
                    unicode(str(lat), "utf8"),
                    unicode(str(lon), "utf8"),

                    unicode(str(cos_lat), "utf8"),
                    unicode(str(sin_lat), "utf8"),

                    unicode(str(cos_lon), "utf8"),
                    unicode(str(sin_lon), "utf8"),

                    unicode(station, "utf8")
                ]

                curs.execute("""
                             INSERT INTO STATIONS \
                             (lat, lon, cos_lat, sin_lat,\
                             cos_lon, sin_lon, station) \
                             VALUES (?, ?, ?, ?, ?, ?, ?);\
                             """, to_db)
            except IndexError:
                print row
                continue

        conn.commit()
    except (csv.Error, UnicodeDecodeError):
        print "error", f
        continue