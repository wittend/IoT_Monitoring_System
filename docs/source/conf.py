# SPDX-License-Identifier: GPL-3.0-or-later
# Configuration file for the Sphinx documentation builder.

import os
import sys
import subprocess
from datetime import datetime

# -- Project information -----------------------------------------------------
project = 'mag-xiao-s3'
author = 'David Witten and contributors'
current_year = str(datetime.now().year)
copyright = f"{current_year}, {author}"

# -- General configuration ---------------------------------------------------
language = 'en'
locale_dirs = ['locales/']   # path is relative to conf.py
gettext_compact = False     # optional
# sphinx-intl needs this to find locale_dirs if it's not explicitly passed
# but it should be able to read it from conf.py
# If it fails, we might need to pass it via CLI

extensions = [
    'myst_parser',
    'sphinx_copybutton',
    'breathe',
]

myst_enable_extensions = [
    'colon_fence',
    'substitution',
]

# Templates path
templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'
html_static_path = ['_static']

# -- Doxygen / Breathe integration ------------------------------------------
# Try to run Doxygen to generate XML for Breathe if available.
this_dir = os.path.abspath(os.path.dirname(__file__))
repo_root = os.path.abspath(os.path.join(this_dir, '..', '..'))
doxyfile_path = os.path.join(repo_root, 'Doxyfile')
doxygen_out = os.path.join(repo_root, 'docs', 'doxygen')
xml_dir = os.path.join(doxygen_out, 'xml')

# Logging helper for nicer messages on RTD/local
try:
    from sphinx.util import logging as sphinx_logging
    logger = sphinx_logging.getLogger(__name__)
except Exception:  # Fallback if Sphinx logging isn't available yet
    class _Logger:
        def warning(self, *a, **k):
            print('[docs] WARNING:', *a)
    logger = _Logger()

# Attempt to run Doxygen if available; ignore failures so local builds still work
if os.path.exists(doxyfile_path):
    try:
        subprocess.run(['doxygen', doxyfile_path], check=False)
    except Exception as e:
        logger.warning('Doxygen invocation failed (%s); proceeding without API docs.', e)

# Configure Breathe only if the XML output exists
if os.path.exists(os.path.join(xml_dir, 'index.xml')):
    breathe_projects = {
        'mag-xiao-s3': xml_dir,
    }
    breathe_default_project = 'mag-xiao-s3'
else:
    # No XML available: skip API pages to avoid build errors on RTD/local
    logger.warning('Doxygen XML not found at %s; API reference will be skipped.', xml_dir)
    exclude_patterns.append('api.rst')
