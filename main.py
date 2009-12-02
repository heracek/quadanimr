#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import django

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')
        self.response.out.write(django.__file__)


application = webapp.WSGIApplication([('/', MainHandler)],
                       debug=True)
def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
