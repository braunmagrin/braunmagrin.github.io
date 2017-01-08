#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Matheus Braun Magrin'
SITENAME = "braunmagrin's Blog"
# SITEURL = 'http://braunmagrin.com/'

PATH = 'content'
STATIC_PATHS = ['images']

# Timezone and locale settings
TIMEZONE = 'America/Sao_Paulo'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MD_EXTENSIONS = ['footnotes']

# Social widget
SOCIAL = (
    ('Facebook', 'https://www.facebook.com/braunmagrin'),
    ('LinkedIn', 'https://br.linkedin.com/in/braunmagrin/en'),
    ('GitHub', 'https://github.com/braunmagrin'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = 'cebong'
# SITETAGLINE = "Text to be displayed below the site's title"
# FOOTERTEXT = "TEXT to be displayed in the footer"

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = []

TIPOGRIFY = True

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>[^_]*)'
SLUGIFY_SOURCE = 'title'
