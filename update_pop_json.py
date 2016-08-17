#!/usr/bin/env python

import sys
import json

json_file = sys.argv[1]
update_file = sys.argv[2]
out_file = sys.argv[3]


state = {}
with open(update_file, "r") as ifd1:
    for line in ifd1:
        line = line.strip()
        tokens = line.split(",")
        if len(tokens) != 3:
            print "Invalid line in state totals file"
            sys.exit(1)
        state[tokens[0]] = [tokens[1], tokens[2]]

with open(json_file, "r") as ifd2:
    pop_json = json.load(ifd2)
    for feat in pop_json["features"]:
        votes = state[feat["properties"]["name"]]
        feat["properties"]["pop8"] = [int(votes[0]),int(votes[1])]
    with open(out_file, "w") as ofd:
        json.dump(pop_json, ofd)
