# -*- coding: utf-8 -*-
#

import sys
import os

sys.path.insert(0, os.path.abspath('../../'))
import djlimiter

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

source_suffix = '.rst'
master_doc = 'index'
project = u'djlimiter'
copyright = u'2015, Ali-Akber Saifee'

version = release = djlimiter.__version__
exclude_patterns = []

htmlhelp_basename = 'djlimiterdoc'

latex_documents = [
    ('index', 'djlimiter.tex', u'Django-Limiter Documentation',
     u'Ali-Akber Saifee', 'manual'),
]
man_pages = [
    ('index', 'django-limiter', u'djlimiter Documentation',
     [u'Ali-Akber Saifee'], 1)
]

texinfo_documents = [
    ('index', 'djlimiter', u'Django-Limiter Documentation',
     u'Ali-Akber Saifee', 'djlimiter', 'One line description of project.',
     'Miscellaneous'),
]

intersphinx_mapping = {'python': ('http://docs.python.org/', None)
    , 'django': ("http://django.readthedocs.org/en/latest", None)
}

autodoc_default_flags = [
    "members"
    , "show-inheritance"
]
