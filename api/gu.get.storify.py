#!/usr/bin/env python
import os
import simplejson
from admin.functions import get_query_string
from admin.models import StorifySnapshots

args = get_query_string(os.environ['QUERY_STRING'])

if 'hashtag' in args:
    hashtag = args['hashtag']
else:
    hashtag = 'default'

#   get the record from the database
snapshot = StorifySnapshots.gql("WHERE hashtag = :1 ORDER BY last_update DESC LIMIT 1", hashtag)

newResult = {}

if snapshot.count() == 0:
    newResult['stat'] = 'error'
    newResult['error'] = '100: no records found with that hastag'
else:
    newResult['stat'] = 'ok'
    newResult['result'] = simplejson.loads(snapshot[0].json)

print 'Content-Type: application/json; charset=UTF-8'
print ''
print simplejson.dumps(newResult)
