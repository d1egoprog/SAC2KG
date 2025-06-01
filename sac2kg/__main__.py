#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
This module provides a command-line interface for converting SAC and JSON files
into Knowledge Graphs following the VEO Schema. It supports processing individual
files or entire directories, with options to include an ontology/schema and specify
output formats.

The main functionality includes:
- Parsing command-line arguments to determine input/output paths, formats, and options.
- Converting individual SAC or JSON files into Knowledge Graphs.
- Recursively processing directories to convert all recognized files while preserving
    the folder structure.

Dependencies:
- __init__.py: Contains the main entry point for the package.
- sac2kg.graph_builder: Provides functions for reading SAC/JSON files and storing
    the resulting Knowledge Graphs.
- sac2kg.sac_reader: Provides functions for reading SAC files.
- sac2kg.veo_definitions: Provides definitions for the VEO schema.
- sac2kg.veo:mapper: Provides functions for mapping SAC/JSON data to the VEO schema.
- sac2kg.veo_model: Provides the VEO model for representing Knowledge Graphs.

Usage:
Run the script with the required arguments to convert files or directories into
Knowledge Graphs. Use the `-h` flag for detailed usage instructions.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
"""

import os
from dotenv import load_dotenv
from importlib.resources import files
load_dotenv(files('').joinpath('.env'))

BUILD_DATE = os.getenv('BUILD_DATE')
AUTHOR_NAME = os.getenv('AUTHOR_NAME')
COMPONENT_VERSION = os.getenv('COMPONENT_VERSION')

__author__ = AUTHOR_NAME
__date__ = BUILD_DATE
__version__ = COMPONENT_VERSION
__copyright__ = "Copyright 2024, Diego Rincon-Yanez"
__status__ = "Prototype"
__deprecated__ = False

import os

from sac2kg.graph_builder import read_from_json, read_from_sac
from sac2kg.graph_builder import graph_store

from tqdm import tqdm

import argparse

parser = argparse.ArgumentParser(
    description='Convert SAC and JSON files into RDF Knowledge Graphs following the VEO Schema')
parser.add_argument('trace_file', type=str, 
    help='Path to the input trace file (SAC or JSON) or directory containing trace files if -d is specified.')
parser.add_argument('kg_file', type=str, 
    help='Path to the output knowledge graph file or directory where the results will be stored if -d is specified.')
parser.add_argument('-f', '--format', type=str, choices=['sac', 'json'], default='sac', 
    help='Supported formats, default=sac. Options: sac or json')
parser.add_argument('-o', '--output', type=str, choices=['n3', 'ttl','rdf'], default='ttl', 
    help='Output formats (NTriples, Turtle, RDF), default=TTL')
parser.add_argument('-s', '--schema', action='store_true',
    help='Include the Ontology/Schema in the knowledge graph')
parser.add_argument('-d', '--directory', action='store_true',
    help='Navigate through a folder structure and convert the recognized files, Replicates the folder structure, only SAC files')
args = parser.parse_args()

@staticmethod
def convert_file(origin_file, dest_file, flags, origin_folder='', dest_folder=''):
    if origin_folder != '':
        origin_file = os.path.join(origin_folder, origin_file)
    if dest_folder != '':
        dest_file = os.path.join(dest_folder, dest_file)

    graph = flags[4](origin_file, ontology=flags[2])
    if graph is None:
        return
    graph_store(graph, dest_file, flags[1])

@staticmethod
def convert_folder(origin_folder, dest_folder, flags):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    fileList = os.listdir(origin_folder)
    for single_file in tqdm(fileList, desc=f'Converting Files in {origin_folder}'):
        new_file = os.path.join(origin_folder, single_file)
        if (os.path.isdir(new_file)):
            new_dest = os.path.join(dest_folder, single_file)
            convert_folder(new_file, new_dest, flags)
        elif (os.path.isfile(new_file)):
            convert_file(single_file, single_file, flags, origin_folder=origin_folder, dest_folder=dest_folder)
    return

if __name__ == "__main__":
    flags = [args.format, args.output, args.schema, args.directory]

    if flags[0] == 'sac':
        flags.append(read_from_sac)
    elif flags[0] == 'json':
        flags.append(read_from_json)

    #Convert a Folder
    if args.directory:
        print(f'... Converting folder {args.trace_file} and everything in it')
        convert_folder(args.trace_file, args.kg_file, flags)
    else:
        print(f'... Converting file {args.trace_file} into VEO KG into a {args.output} format')
        convert_file(args.trace_file, args.kg_file, flags)
