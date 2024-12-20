#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Some module docs

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
__version__ = "0.2"

import os

from alive_progress import alive_bar

import argparse
parser = argparse.ArgumentParser(description='Convert SAC and JSON files into Knowledge Graphs followinf teh VEO Schema')
parser.add_argument('-f', '--folder', type=str, help='Navigate trougth a folder structure and convert the recognized files')
parser.add_argument('--file', type=str, help='Convert a single file')
args = parser.parse_args()

if __name__ == "__main__":
    print("Converting SAC Files to KG using the VEO Ontology")
    print(args.folder, args.file)
    if args.folder != None :
        #Convert a Folder
        print(f'..converting folder {args.folder} and everything in it')
    elif args.folder == None:
        #Convert a Single File
        print(f'..converting file {args.file}')
    else:
        print("Unsupported Generation Format")
        parser.print_help()
