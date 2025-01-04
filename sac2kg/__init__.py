#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Init the packages

Longer description of this module is not made yet :).

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
"""

__author__ = "Diego Rincon-Yanez"
__copyright__ = "Copyright 2024, Diego Rincon-Yanez"
__date__ = "2024/10/20"
__deprecated__ = False
__status__ = "Prototype"
__version__ = '0.3.1'

from importlib.resources import files
from dotenv import load_dotenv

load_dotenv(files('sac2kg').joinpath('.env'))

from sac2kg.graph_builder import read_from_json
from sac2kg.graph_builder import read_from_sac
from sac2kg.graph_builder import graph_store



