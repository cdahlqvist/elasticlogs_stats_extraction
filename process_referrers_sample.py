#!/usr/bin/python

import json
import sys
import re

threshold = 100

sample_size = 1000
sample_count = 0

inputfile = open('./statistics/referrers.json', 'r')

data = inputfile.read()

obj = json.loads(data)

referrers = []
path_lookup = {}
path_lookup_id = 0

unique_referrers_count = 0
referrers_count = 0
unique_filtered_count = 0
filtered_count = 0

for value in obj:
    count = value['count']
    value.pop('count', None)

    if count > threshold and sample_count < sample_size:
        sample_count += 1
        referrers_count += count
        unique_referrers_count += 1

        m = re.match("^((?:.*?/){1,5})(.*)", value['referrer'])

        if m:
            path = m.groups(1)[0]
            rest = m.groups(1)[1]

        else:
            path = value['referrer']
            rest = ""

        if path in path_lookup:
            path_id = path_lookup[path]
        else:
            path_lookup[path] = str(path_lookup_id)
            path_id = str(path_lookup_id)
            path_lookup_id += 1

        referrers.append([count, [path_id, rest]])

    else:
        filtered_count += count
        unique_filtered_count += 1

# Reverse lookups
path_lookup = {v: k for k, v in path_lookup.items()}

outputfile = open('./config/referrers_data_sample.js', 'w')

outputfile.write("/* Items in the referrers list has the following structure: [<count>, [<url lookup id>, <url suffix>]] */\n\n")
outputfile.write("module.exports.referrers = ")
outputfile.write(json.dumps(referrers, separators=(',', ':')))
outputfile.write(";\n\nmodule.exports.url_base_lookup = ")
outputfile.write(json.dumps(path_lookup, separators=(',', ':')))
outputfile.write(";")

outputfile.close()

total = referrers_count + filtered_count

sys.stdout.write('Unique referrers count: {}\n'.format(unique_referrers_count))
sys.stdout.write('Unique filtered count: {}\n'.format(unique_filtered_count))
sys.stdout.write('Referrers count: {} ({})\n'.format(referrers_count, referrers_count * 100.0 / total))
sys.stdout.write('Filtered count: {} ({})\n'.format(filtered_count, filtered_count * 100.0 / total))

