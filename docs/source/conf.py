from pathlib import Path

# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

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
with open(BASE_DIR / 'VERSION') as version_file:
    version = version_file.read().strip()

# The full project version.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-release
release = version


# Options for HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme
html_theme = 'default'
