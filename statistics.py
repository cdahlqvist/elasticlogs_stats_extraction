#!/usr/bin/python

import json
import sys
import re

def write_to_file(datamap, filename):
    file = open(filename, "w")
    file.write(json.dumps(datamap))
    file.close()

def dict_to_list (datamap):
    objlist = []

    for key, value in datamap.iteritems():
        objlist.append(value)

    return objlist

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
            if obj['clientip'] in clientips:
                clientips[obj['clientip']]['count'] += 1
            else :
                clientips[obj['clientip']] = {}
                clientips[obj['clientip']]['count'] = 1
                clientips[obj['clientip']]['clientip'] = obj['clientip']
                clientips[obj['clientip']]['geoip'] = obj['geoip']


        #request = obj['verb'] + " " + obj['httpversion'] + " " + obj['request'] + " " + obj['response'] + " " + obj['bytes']
        request = '{} {} {} {} {}'.format(obj['verb'], obj['request'], obj['httpversion'], obj['response'], obj['bytes'])

        if request in requests:
    	    requests[request]['count'] += 1
        else:
    	    requests[request] = {}
            requests[request]['count'] = 1
            requests[request]['verb'] = obj['verb']
            requests[request]['httpversion'] = obj['httpversion']
            requests[request]['request'] = obj['request']
            requests[request]['response'] = obj['response']
            requests[request]['bytes'] = obj['bytes']

        if obj['agent'].startswith('"') and obj['agent'].endswith('"'):
            agent = obj['agent'][1:-1]
        else:
            agent = obj['agent']

        if agent == "-":
            agent_key = "underscore_"
        else:
            agent_key = agent

        if agent_key in agents:
    	    agents[agent_key]['count'] += 1
        else :
    	    agents[agent_key] = {}
    	    agents[agent_key]['count'] = 1
            agents[agent_key]['agent'] = agent
    	    agents[agent_key]['useragent'] = obj['useragent']
    
        if obj['referrer'].startswith('"') and obj['referrer'].endswith('"'):
            referrer = obj['referrer'][1:-1]
        else:
            referrer = obj['referrer']

        if referrer == "-":
            referrer_key = "underscore_"
        else:
            referrer_key = referrer

        if referrer_key in referrers:
    	    referrers[referrer_key]['count'] += 1
        else:
            referrers[referrer_key] = {}
    	    referrers[referrer_key]['count'] = 1
            referrers[referrer_key]['referrer'] = referrer

        counter += 1
        if counter % 1000000 == 0:
            print "Processed %d records" % counter

    except ValueError:
        pass

# Write all statistics to files in JSON format
write_to_file(dict_to_list(clientips), "clientips.json")
write_to_file(dict_to_list(agents), "agents.json")
write_to_file(dict_to_list(requests), "requests.json")
write_to_file(dict_to_list(referrers), "referrers.json")

