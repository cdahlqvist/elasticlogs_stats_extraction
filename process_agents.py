#!/usr/bin/python

import json
import sys

inputfile = open('./statistics/agents.json', 'r')

data = inputfile.read()

obj = json.loads(data)

agents = []
os_lookup = {}
os_lookup_id = 0
os_name_lookup = {}
os_name_lookup_id = 0
name_lookup = {}
name_lookup_id = 0

unique_agents_count = 0
agents_count = 0
filtered_count = 0

for value in obj:
    count = value['count']
    value.pop('count', None)

    if 'major' in value['useragent']:
        del value['useragent']['major']

    if 'minor' in value['useragent']:   
        del value['useragent']['minor']

    if 'patch' in value['useragent']:
        del value['useragent']['patch']
    
    if 'device' in value['useragent']:
        del value['useragent']['device']

    if 'os_major' in value['useragent']:
        del value['useragent']['os_major']

    if 'os_minor' in value['useragent']:
        del value['useragent']['os_minor']

    if 'build' in value['useragent']:
        del value['useragent']['build']

    if count > 500:
        agents_count += count
        unique_agents_count += 1

        item = [count, value['agent']]

        if 'os' in value['useragent']:
            if value['useragent']['os'] in os_lookup:
                item.append(os_lookup[value['useragent']['os']])
            else:
                os_lookup[value['useragent']['os']] = str(os_lookup_id)
                item.append(str(os_lookup_id))
                os_lookup_id += 1
        else:
            item.append('')

        if 'os_name' in value['useragent']:
            if value['useragent']['os_name'] in os_name_lookup:
                item.append(os_name_lookup[value['useragent']['os_name']])
            else:
                os_name_lookup[value['useragent']['os_name']] = str(os_name_lookup_id)
                item.append(str(os_name_lookup_id))
                os_name_lookup_id += 1
        else:
            item.append('')

        if 'name' in value['useragent']:
            if value['useragent']['name'] in name_lookup:
                item.append(name_lookup[value['useragent']['name']])
            else:
                name_lookup[value['useragent']['name']] = str(name_lookup_id)
                item.append(str(name_lookup_id))
                name_lookup_id += 1
        else:
            item.append('')

        agents.append(item)

    else:
        filtered_count += count

# Reverse lookups
os_lookup = {v: k for k, v in os_lookup.items()}
os_name_lookup = {v: k for k, v in os_name_lookup.items()}
name_lookup = {v: k for k, v in name_lookup.items()}

outputfile = open('./config/agents_data.js', 'w')

outputfile.write("/* Items in the agents list has the following structure: [<count>, <agent>, <useragent.os lookup id>, <useragent.os_name lookup id>, <useragent.name lookup id>] */\n\n")
outputfile.write("module.exports.agents = ")
outputfile.write(json.dumps(agents, separators=(',', ':')))
outputfile.write(";\n\nmodule.exports.os_lookup = ")
outputfile.write(json.dumps(os_lookup, separators=(',', ':')))
outputfile.write(";\n\nmodule.exports.os_name_lookup = ")
outputfile.write(json.dumps(os_name_lookup, separators=(',', ':')))
outputfile.write(";\n\nmodule.exports.name_lookup = ")
outputfile.write(json.dumps(name_lookup, separators=(',', ':')))
outputfile.write(";")

outputfile.close()

total = agents_count + filtered_count

sys.stdout.write('Unique agent count: {}\n'.format(unique_agents_count))
sys.stdout.write('Agent count: {} ({})\n'.format(agents_count, agents_count * 100.0 / total))
sys.stdout.write('Filtered count: {} ({})\n'.format(filtered_count, filtered_count * 100.0 / total))

