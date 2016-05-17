#!/usr/bin/python

import json
import sys
import re

def write_to_file(datamap, filename):
    file = open(filename, "w")
    file.write(json.dumps(datamap))
    file.close()

counter = 0

# Per clientip prefix, count and geoip data 
clientips = {}

# For each agent store count and resulting userdata
agents = {}

# merge request to string and store count per request
requests = {}

# Store referrers and counts
referrers = {}

for line in sys.stdin:
    try:
        obj = json.loads(line)

        if 'geoip' in obj:
            clientip_prefix = re.search(r'^(\d+\.\d+\.\d+)', obj['clientip']).group()
            
            if clientip_prefix in clientips:
                clientips[clientip_prefix]['count'] += 1
            else :
                clientips[clientip_prefix] = {}
                clientips[clientip_prefix]['count'] = 1
            clientips[clientip_prefix]['geoip'] = obj['geoip']

        #request = obj['verb'] + " " + obj['httpversion'] + " " + obj['request'] + " " + obj['response'] + " " + obj['bytes']
        request = '{} {} {} {} {}'.format(obj['verb'], obj['request'], obj['httpversion'], obj['response'], obj['bytes'])

        if request in requests:
    	    requests[request]['count'] += 1
        else:
    	    requests[request] = {}
            requests[request]['count'] = 1
            requests[request]['data'] = {}
            requests[request]['data']['verb'] = obj['verb']
            requests[request]['data']['httpversion'] = obj['httpversion']
            requests[request]['data']['request'] = obj['request']
            requests[request]['data']['response'] = obj['response']
            requests[request]['data']['bytes'] = obj['bytes']

        if obj['agent'] in agents:
    	    agents[obj['agent']]['count'] += 1
        else :
    	    agents[obj['agent']] = {}
    	    agents[obj['agent']]['count'] = 1
    	    agents[obj['agent']]['useragent'] = obj['useragent']
    
        if obj['referrer'] in referrers:
    	    referrers[obj['referrer']] += 1
        else:
    	    referrers[obj['referrer']] = 1

        counter += 1
        if counter % 1000000 == 0:
            print "Processed %d records" % counter

    except ValueError:
        pass

# Write all statistics to files in JSON format
write_to_file(clientips, "clientips.json")
write_to_file(agents, "agents.json")
write_to_file(requests, "requests.json")
write_to_file(referrers, "referrers.json")

