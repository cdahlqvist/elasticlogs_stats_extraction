#!/usr/bin/python

import json
import sys
import re

threshold = 500

sample_size = 1000
sample_count = 0

inputfile = open('./statistics/clientips.json', 'r')

data = inputfile.read()

obj = json.loads(data)

clientips = []
country_lookup = {}
country_lookup_id = 0
location_lookup = {}
location_key_lookup = {}
location_lookup_id = 0

rare_clientips_lookup = {}

unique_clientip_count = 0
clientip_count = 0
unique_rare_count = 0
rare_count = 0
prefix_count = 0

for value in obj:
    count = value['count']
    value.pop('count', None)

    if sample_count < sample_size:
        sample_count += 1

        if count > threshold:
            unique_clientip_count += 1
            clientip_count += count

            item = [count, value['clientip']]

            if 'country_name' in value['geoip']:
                if value['geoip']['country_name'] in country_lookup:
                    item.append(country_lookup[value['geoip']['country_name']])
                else:
                    country_lookup[value['geoip']['country_name']] = str(country_lookup_id)
                    item.append(str(country_lookup_id))
                    country_lookup_id += 1
            else:
                item.append('')

            if 'location' in value['geoip']:
                location_key = "{:3.3f}_{:3.3f}".format(value['geoip']['location'][0], value['geoip']['location'][1])
        
                if location_key in location_key_lookup:
                    item.append(location_key_lookup[location_key])
                else:

                    location_key_lookup[location_key] = str(location_lookup_id)
                    location_lookup[str(location_lookup_id)] = value['geoip']['location']
                    item.append(str(location_lookup_id))
                    location_lookup_id += 1

            clientips.append(item)

        else:
            rare_count += count
            unique_rare_count += 1

            m = re.match("^(\d{1,3}\.\d{1,3})\.", value['clientip'])

            ip_prefix = m.groups(1)

            if 'country_name' in value['geoip']:
                if value['geoip']['country_name'] in country_lookup:
                    country_id = country_lookup[value['geoip']['country_name']]
                else:
                    country_lookup[value['geoip']['country_name']] = str(country_lookup_id)
                    country_id = str(country_lookup_id)
                    country_lookup_id += 1
            else:
                country_id = ''

            if 'location' in value['geoip']:
                location_key = "{:3.3f}_{:3.3f}".format(value['geoip']['location'][0], value['geoip']['location'][1])
        
                if location_key in location_key_lookup:
                    location_id= location_key_lookup[location_key]
                else:

                    location_key_lookup[location_key] = str(location_lookup_id)
                    location_lookup[str(location_lookup_id)] = value['geoip']['location']
                    location_id = str(location_lookup_id)
                    location_lookup_id += 1
        
            if ip_prefix not in rare_clientips_lookup:
                rare_clientips_lookup[ip_prefix] = { 'count': 0 }
                prefix_count += 1

            rare_clientips_lookup[ip_prefix]['count'] += count
            rare_clientips_lookup[ip_prefix]['prefix'] = ip_prefix

            if country_id in rare_clientips_lookup[ip_prefix]:
                rare_clientips_lookup[ip_prefix][country_id]['count'] += count

                if location_id not in rare_clientips_lookup[ip_prefix][country_id]['locations']:
                    rare_clientips_lookup[ip_prefix][country_id]['locations'].append(location_id)

            else:
                rare_clientips_lookup[ip_prefix][country_id] = { 'count': count, 'locations': [location_id] }


# Reverse lookups
country_lookup = {v: k for k, v in country_lookup.items()}

# Convert rare clientips lookup to list
rare_clientips = []
for prefix in rare_clientips_lookup:
    rare_clientips.append(rare_clientips_lookup[prefix])

total = clientip_count + rare_count

outputfile = open('./config/clientips_data_sample.js', 'w')

outputfile.write("/* Items in the clientips list has the following structure: [<count>, <ip>, <geoip.country_name lookup id>, <geoip.location lookup id>, <useragent.name lookup id>] */\n\n")
outputfile.write("module.exports.clientips = ")
outputfile.write(json.dumps(clientips, separators=(',', ':')))
outputfile.write(";\n\nmodule.exports.rare_clientips = ")
outputfile.write(json.dumps(rare_clientips, separators=(',', ':')))
outputfile.write(";\n\nmodule.exports.country_lookup = ")
outputfile.write(json.dumps(country_lookup, separators=(',', ':')))
outputfile.write(";\n\nmodule.exports.location_lookup = ")
outputfile.write(json.dumps(location_lookup, separators=(',', ':')))
outputfile.write(";\n\nmodule.exports.rare_clientip_probability = {};".format(rare_count/total))

outputfile.close()

sys.stdout.write('Count threshold: {}\n'.format(threshold))
sys.stdout.write('Unique agent count: {}\n'.format(unique_clientip_count))
sys.stdout.write('Unique rare count: {}\n'.format(unique_rare_count))
sys.stdout.write('Clientip count: {} ({})\n'.format(clientip_count, clientip_count * 100.0 / total))
sys.stdout.write('Rare count: {} ({})\n'.format(rare_count, rare_count * 100.0 / total))
sys.stdout.write('Rare prefix count: {}\n'.format(prefix_count))

#x [0,1]
#=CEILING(B2*(1-B2)*255*4, 1)





