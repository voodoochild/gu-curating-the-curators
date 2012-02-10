#!/usr/bin/env python
from admin.models import StorifySnapshots

#   get the record from the database
snapshot = StorifySnapshots.gql("ORDER BY last_update DESC LIMIT 1")

print 'Content-Type: application/json; charset=UTF-8'
print ''
print snapshot[0].json
