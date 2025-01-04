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

import json

from rdflib import Graph

from sac2kg.veo_mapper import VEOSemanticMapper
from sac2kg.veo_model import *
from sac2kg.sac_reader import SAC2VEO


@staticmethod
def read_from_sac(path, ontology=False):
    data_model = SAC2VEO._parse_file(path)
    gm = GraphManager(data_model)
    graph = gm.get_rdf_graph(ontology)
    return graph

@staticmethod
def read_from_json(path, ontology=False):
    with open(path, 'r') as file:
        data_model = json.load(file)
    gm = GraphManager(data_model)
    graph = gm.get_rdf_graph(ontology)
    return graph

@staticmethod
def graph_store(graph, name='populated-kg', output='ttl'):
    """
    Stores the given graph in a persistent storage with the specified name.

    Parameters:
        graph: rdflib.Graph
            The RDF graph to store.
        name: str, optional
            The name under which the graph will be saved. Defaults to 'populated-kg'.

    Returns:
        None
    """
    if output == 'ttl':
        with open(f'{name}.ttl', 'w', encoding='utf8') as f:
            f.write(graph.serialize(format='turtle'))
    elif output == 'n3':
        with open(f'{name}.n3', 'w', encoding='utf8') as f:
            f.write(graph.serialize(format='ntriples'))
    elif output == 'rdf':
        with open(f'{name}.rdf', 'w', encoding='utf8') as f:
            f.write(graph.serialize(format='xml'))
    else:
        print("Unsupported Knowledge Graph output Format")
        exit(0)

class GraphManager:

    def __init__(self, model=(dict|None), graph=(Graph|None)):
        if model != None:
            self.data_model = model
        if graph != None:
            self.graph = graph

    def get_rdf_graph(self, schema : bool):
        model = VEORDF(**self.data_model)
        mapper = VEOSemanticMapper(schema=schema)
        graphCon = mapper.get_context_model(mapper.veo_graph, model)
        graphCol = mapper.get_collection_model(graphCon, model)
        self.graph = mapper.get_knowledge_model(graphCol, model)
        return self.graph
    
    def get_neo4j_graph(self):
        return self.graph
    
    def save(self, name='populated-kg', output='ttl'):
        graph_store(self.graph, name, output)

    def __str__(self):
        return self.graph.serialize(format='turtle')
    
    
