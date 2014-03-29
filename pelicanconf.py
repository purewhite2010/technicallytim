#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

THEME = "/home/tim/pelican-themes/pelican-sundown"

PLUGIN_PATH = '/home/tim/pelican-plugins/'
#PLUGINS = ['assets']

DISQUS_SITENAME = 'technicallytim.disqus.com'

AUTHOR = u'Tim White'
SITENAME = u'Technically Tim'
SITEURL = ''

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}.html'

TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}.html'



YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

TIMEZONE = 'Australia/Brisbane'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Old Blog', 'http://weirdo.purewhite.id.au/'),
          ('Family Blog', 'http://purewhite.id.au'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
PIWIK_URL = 'piwik.purewhite.id.au'
PIWIK_SITE_ID = 4 


#STATIC_PATHS = ['images', 'extra/CNAME']
#EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
