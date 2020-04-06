"""GAME - An opinionated, minimal cookiecutter template for Python packages"""

import pkg_resources

from . import helpers
from . import assignment
from . import questionGui
from . import texMaker


__version__ = '0.1.0'
__author__ = '\Ashkan Shokri <ashkan.shokri@gmail.com>'
__all__ = ['helpers', 'assignment', 'questionGui', 'texMaker']




# __name__ in case you're within the package
# - otherwise it would be 'lidtk' in this example as it is the package name
path = 'CURSUS.cls'  # always use slash
clsFile = pkg_resources.resource_filename(__name__, path)    