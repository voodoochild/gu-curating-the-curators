#!/usr/bin/env python
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template


################################################################################
################################################################################
#
# End of messy include stuff
#
################################################################################
################################################################################


class MainHandler(webapp.RequestHandler):
    def get(self):

        template_values = {
            'msg': 'hello world'
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
