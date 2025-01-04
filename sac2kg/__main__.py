#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 

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
__version__ = "0.3.1"

import os

from sac2kg.graph_builder import read_from_json, read_from_sac
from sac2kg.graph_builder import graph_store

from tqdm import tqdm

import argparse

parser = argparse.ArgumentParser(
    description='Convert SAC and JSON files into Knowledge Graphs following the VEO Schema')
parser.add_argument('traceFile', type=str, 
    help='Path to the input trace file (SAC or JSON) or directory containing trace files if -d is specified.')
parser.add_argument('kgFile', type=str, 
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
        dest_file = os.path.join(dest_folder,dest_file)

    graph = flags[4](origin_file, ontology=flags[2])
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
        print(f'... Converting folder {args.traceFile} and everything in it')
        convert_folder(args.traceFile, args.kgFile, flags)
    else:
        print(f'... Converting file {args.traceFile} into VEO KG into a {args.output} format')
        convert_file(args.traceFile, args.kgFile, flags)
