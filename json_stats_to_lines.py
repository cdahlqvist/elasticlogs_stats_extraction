#!/usr/bin/python

import json
import sys

for line in sys.stdin:
    obj = json.loads(line)

    for value in obj:
        count = value['count']
        value.pop('count', None)

        sys.stdout.write('{}:{}\n'.format(count, json.dumps(value)))
    
