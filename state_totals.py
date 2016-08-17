#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
    print "Usage: " + sys.argv[0] + " <county-csv>"
    sys.exit(1)

county_csv = sys.argv[1]

per_count_list = []
header = False
with open(county_csv, "r") as ifd:
    for line in ifd:
        if not header:
            header = True
            continue
         line = line.strip()
         tokens = line.split(",")
         if len(tokens) != 3:
             print "Invalid line in county csv"
             sys.exit(1)
          fips = tokens[0]
          dems = int(tokens[1])
          rep = int(tokens[2])
          per_county = {fips, dems, rep}
          per_county_list.append(per_county)


