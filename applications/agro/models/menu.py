# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Radu Ioan Fericean <radu@fericean.ro>'
response.meta.description = 'usamv apps'
response.meta.keywords = 'usamvbt, usab, timisoara, romania, agricultura'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]
