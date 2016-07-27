#!/usr/bin/python

import json
import sys
import re

threshold = 200

inputfile = open('./statistics/requests.json', 'r')

data = inputfile.read()

obj = json.loads(data)

requests = []
path_lookup = {}
path_lookup_id = 0

unique_requests_count = 0
requests_count = 0
unique_filtered_count = 0
filtered_count = 0

for value in obj:
    count = value['count']
    value.pop('count', None)

    if count > threshold or (count> 10 and value['response'] != 200):
        requests_count += count
        unique_requests_count += 1

        m = re.match("^((.*/){1,5})(.*)", value['request'])

        if m:
            path = m.groups()[0]
            rest = m.groups()[1]

        else:
            path = value['request']
            rest = ""

        if path in path_lookup:
            path_id = path_lookup[path]
        else:
            path_lookup[path] = str(path_lookup_id)
            path_id = str(path_lookup_id)
            path_lookup_id += 1

        item = [count, path_id, rest, value['bytes'], value['verb'], value['response'], value['httpversion']]

        requests.append(item)

    else:
        filtered_count += count
        unique_filtered_count += count

# Reverse lookups
path_lookup = {v: k for k, v in path_lookup.items()}

outputfile = open('./config/requests_data.js', 'w')

outputfile.write("/* Items in the requests list has the following structure: [<count>, <url base lookup id, <url suffix>, <bytes>, <verb> <response>, <httpversion>] */\n\n")
outputfile.write("module.exports.requests = ")
outputfile.write(json.dumps(requests, separators=(',', ':')))
outputfile.write(";\n\nmodule.exports.url_base_lookup = ")
outputfile.write(json.dumps(path_lookup, separators=(',', ':')))
outputfile.write(";")

outputfile.close()

total = requests_count + filtered_count

sys.stdout.write('Unique requests count: {}\n'.format(unique_requests_count))
sys.stdout.write('Unique filtered count: {}\n'.format(unique_filtered_count))
sys.stdout.write('Requests count: {} ({})\n'.format(requests_count, requests_count * 100.0 / total))
sys.stdout.write('Filtered count: {} ({})\n'.format(filtered_count, filtered_count * 100.0 / total))

