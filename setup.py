#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The setup for the package

Longer description of this module is not made yet :).

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
"""

VERSION = '0.3.3'

__author__ = "Diego Rincon-Yanez"
__copyright__ = "Copyright 2024, Diego Rincon-Yanez"
__date__ = "2024/10/20"
__deprecated__ = False
__status__ = "Prototype"
__version__ = VERSION

import sys
from setuptools import setup, find_packages

NAME = 'sac2kg'
REQUIRES = ['future>=1.0.0','obspy>=1.4.1','numpy>=2.1.3','rdflib>=7.0.0','tqdm>=4.64.7','python-dotenv>=1.0.1']
DESCIPTION = 'A Python package for generating RDF knowledge graphs based on the Volcano Event Ontology VEO.'
AUTHOR = 'Diego Rincon-Yanez'
AUTHOR_EMAIL = 'rinconyanezd+sac2kg@gmail.com'
URL = 'https://github.com/d1egoprog/sac2kg'
KEYWORDS = ['SAC', 'Knowledge Graph', 'Command Line Interface','NeuroSymbolic AI','Graph Generation']

setup(
    name=NAME,
	version=VERSION,
	description=DESCIPTION,
	author=AUTHOR,
	author_email=AUTHOR_EMAIL,
	url=URL,
	license='MIT',
    packages=find_packages(),
    install_requires=REQUIRES,
    package_data={'': ['*.yml']},
    keywords=KEYWORDS,
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
