import os
import sys
sys.path.insert(0, os.path.abspath('.'))

project = 'XIAO ESP32S3 Edge Data Collector'
copyright = '2026, Dave'
author = 'Dave'
release = '0.1.0'

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'furo'
html_static_path = ['_static']
