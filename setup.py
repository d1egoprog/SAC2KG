# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Setup script for the SAC2KG Python package.

This script uses setuptools to package and distribute the SAC2KG library, 
a tool for generating RDF knowledge graphs based on the Volcano Event Ontology (VEO).

Attributes:
    VERSION (str): The current version of the package.
    __author__ (str): The author of the package.
    __copyright__ (str): Copyright information for the package.
    __date__ (str): The release date of the current version.
    __deprecated__ (bool): Indicates whether the package is deprecated.
    __status__ (str): The development status of the package.
    __version__ (str): Alias for the current version of the package.

Setup Parameters:
    NAME (str): The name of the package.
    REQUIRES (list): A list of required dependencies for the package.
    DESCIPTION (str): A short description of the package.
    AUTHOR (str): The name of the package author.
    AUTHOR_EMAIL (str): The email address of the package author.
    URL (str): The URL of the package's repository or homepage.
    KEYWORDS (list): A list of keywords associated with the package.

The setup function is configured to:
    - Define the package metadata (name, version, author, etc.).
    - Specify the required dependencies.
    - Include additional package data (e.g., YAML files).
    - Define entry points for command-line scripts.
    - Specify the Python version compatibility.
    - Provide a long description from the README file.
    - Classify the package for PyPI.

Usage:
    Run this script using `python setup.py install` to install the SAC2KG package.
"""

import os
from dotenv import load_dotenv
load_dotenv()

BUILD_DATE = os.getenv('BUILD_DATE')

AUTHOR_NAME = os.getenv('AUTHOR_NAME')
AUTHOR_EMAIL = os.getenv('AUTHOR_EMAIL')

COMPONENT_NAME = os.getenv('COMPONENT_NAME')
COMPONENT_VERSION = os.getenv('COMPONENT_VERSION')
COMPONENT_DESCRIPTION = os.getenv('COMPONENT_DESCRIPTION')
COMPONENT_URL = os.getenv('COMPONENT_URL')
COMPONENT_KEYWORDS = os.getenv('COMPONENT_KEYWORDS').split(',')

REQUIRES = ['future>=1.0.0','obspy>=1.4.1','numpy>=2.1.3','rdflib>=7.0.0','tqdm>=4.64.7','python-dotenv>=1.0.1']

__author__ = AUTHOR_NAME
__date__ = BUILD_DATE
__version__ = COMPONENT_VERSION
__copyright__ = "Copyright 2024, Diego Rincon-Yanez"
__status__ = "Prototype"
__deprecated__ = False

from setuptools import setup, find_packages

setup(
    name=COMPONENT_NAME,
	version=COMPONENT_VERSION,
	description=COMPONENT_DESCRIPTION,
	url=COMPONENT_URL,
    keywords=COMPONENT_KEYWORDS,
	author=AUTHOR_NAME,
	author_email=AUTHOR_EMAIL,
	license='MIT',
    packages=find_packages(),
    package_data={'': ['*.yml']},
    install_requires=REQUIRES,
    data_files=[('sac2kg/.env', ['sac2kg/owl/veo.schema.en.5.7.rdf'])],
    include_package_data=True,
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    entry_points={'console_scripts': ['sac2kg=sac2kg.__main__:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
