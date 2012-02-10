#!/usr/bin/env python
import simplejson
from datetime import datetime
from admin.models import StorifySnapshots
from google.appengine.api import urlfetch

#
# Fetch the latest eyewitness image
#
fetchUrl = 'http://api.storify.com/v1/stories/browse/popular?per_page=10'
result = urlfetch.fetch(url=fetchUrl)

resultJSON = simplejson.loads(result.content)
storifyJSON = resultJSON

for story in storifyJSON['content']['stories']:
    del story['stats']['embeds']
    del story['meta']['quoted']

o = datetime.now().toordinal()

newRow = StorifySnapshots()
newRow.ordinal = o
newRow.json = simplejson.dumps(storifyJSON)
newRow.put()
