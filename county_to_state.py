#!/usr/bin/env python

import sys

if len(sys.argv) != 4:
    print "Usage: " + sys.argv[0] + " <county-csv> <state_fips_codes> <outfile>"
    sys.exit(1)

county_csv = sys.argv[1]
state_fips_csv = sys.argv[2]
out_csv = sys.argv[3]

per_county_list = []
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
        repub = int(tokens[2])
        per_county = {"fips": fips, "dems":dems, "repub":repub}
        per_county_list.append(per_county)

state_fips = {}
with open(state_fips_csv, "r") as ifd2:
    for line in ifd2:
        line = line.strip()
        tokens = line.split(",")
        if len(tokens) != 2:
            print "Invalid line in state fips csv"
            sys.exit(2)
        state_code = int(tokens[0])
        state_fips[state_code] = {}
        state_fips[state_code]['name'] = tokens[1]
        state_fips[state_code]['dems'] = 0
        state_fips[state_code]['repub'] = 0


for county in per_county_list:
    state_code = int(county["fips"]) / 1000
    if state_code not in state_fips.keys():
        print "state code: " + str(state_code) + " not found"
    state_fips[state_code]['dems'] += county["dems"]
    state_fips[state_code]['repub'] += county["repub"]

with open(out_csv, "a") as ofd:
    for k,v in state_fips.iteritems():
        ofd.write(v["name"] +"," + str(v["dems"]) + "," + str(v["repub"]) + "\n")
     
