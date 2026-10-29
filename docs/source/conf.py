# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import tomllib
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


# Project information
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# The documented project’s name.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-project
project = 'Python Wrapper for the Ringing Class Library'

# A copyright statement.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-copyright
copyright = '2014-%Y, Leigh Simpson <code@simpleigh.com>'

# The major project version.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-version
with open(BASE_DIR / 'pyproject.toml', 'rb') as pyproject:
    version = tomllib.load(pyproject)['project']['version']

# The full project version.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-release
release = version


# General configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# A list of strings that are module names of Sphinx extensions.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-extensions
extensions = ['sphinx.ext.autodoc']


# Options for HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme
html_theme = 'default'
