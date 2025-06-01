#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sac2kg: A Python library for building and managing knowledge graphs.

This library provides tools to construct knowledge graphs from various data
sources, including JSON and SAC files. It also includes utilities for storing
and querying the resulting graphs.

Environment:
- Automatically loads environment variables from a `.env` file located in the
    `sac2kg` package directory.
"""

import os
from dotenv import load_dotenv
from importlib.resources import files

load_dotenv(files().joinpath('.env'))

BUILD_DATE = os.getenv('BUILD_DATE')
AUTHOR_NAME = os.getenv('AUTHOR_NAME')
COMPONENT_VERSION = os.getenv('COMPONENT_VERSION')

__author__ = AUTHOR_NAME
__date__ = BUILD_DATE
__version__ = COMPONENT_VERSION
__copyright__ = "Copyright 2024, Diego Rincon-Yanez"
__status__ = "Prototype"
__deprecated__ = False

from importlib.resources import files
from dotenv import load_dotenv

load_dotenv(files('sac2kg').joinpath('.env'))

from sac2kg.graph_builder import read_from_json
from sac2kg.graph_builder import read_from_sac
from sac2kg.graph_builder import graph_store



