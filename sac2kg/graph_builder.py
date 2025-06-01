#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides functionality for building and managing RDF graphs 
from various data sources, such as SAC files and JSON files. It includes 
methods for reading data, converting it into RDF graphs, and storing the 
graphs in different serialization formats. The module also defines a 
GraphManager class to handle graph operations and transformations.

Classes:
    - GraphManager: A class to manage RDF graphs, including their creation, 
      transformation, and storage.

Functions:
    - read_from_sac(path, ontology=False): Reads a SAC file and converts it 
      into an RDF graph.
    - read_from_json(path, ontology=False): Reads a JSON file and converts 
      it into an RDF graph.
    - graph_store(graph, name='populated-kg', output='ttl'): Stores the given 
      RDF graph in a persistent storage with the specified name and format.

Dependencies:
    - os: For environment variable handling.
    - dotenv: For loading environment variables from a .env file.
    - json: For handling JSON data.
    - rdflib: For creating and managing RDF graphs.
    - sac2kg.veo_mapper: For mapping data models to RDF graphs.
    - sac2kg.veo_model: For defining the VEO RDF model.
    - sac2kg.sac_reader: For reading SAC files and converting them to VEO data models.
"""

import os
from dotenv import load_dotenv
load_dotenv()

BUILD_DATE = os.getenv('BUILD_DATE')
AUTHOR_NAME = os.getenv('AUTHOR_NAME')
COMPONENT_VERSION = os.getenv('COMPONENT_VERSION')

__author__ = AUTHOR_NAME
__date__ = BUILD_DATE
__version__ = COMPONENT_VERSION
__copyright__ = "Copyright 2024, Diego Rincon-Yanez"
__status__ = "Prototype"
__deprecated__ = False

import json

from rdflib import Graph

from sac2kg.veo_mapper_rdf import VEORDFMapper
from sac2kg.veo_mapper_cypher import VEOCypherMapper
from sac2kg.veo_model import *
from sac2kg.sac_reader import SAC2VEO

class GraphManager:
    """
    GraphManager is a class designed to manage and manipulate graph data structures, 
    specifically RDF and Neo4j graphs. It provides methods for generating RDF graphs 
    using a data model and semantic mapping, retrieving Neo4j graph instances, saving 
    graphs to files in various formats, and serializing graphs into Turtle format.

    Attributes:
        data_model (dict | None): The data model used for graph generation. Defaults to None.
        graph (Graph | None): The graph object managed by this class. Defaults to None.
    
    Methods:
        __init__(model=(dict|None), graph=(Graph|None)):
            Initializes the GraphManager instance with an optional data model and graph.
        get_rdf_graph(schema: bool):
        get_neo4j_graph():
            Retrieves the Neo4j graph instance associated with this object.
        save(name='populated-kg', output='ttl'):
        __str__():
    """

    def __init__(self, model=(dict|None), graph=(Graph|None)):
        """
        Initializes the GraphBuilder instance with an optional data model and graph.
        Args:
            model (dict | None): The data model to be used. Defaults to None.
            graph (Graph | None): The graph object to be used. Defaults to None.
        """

        if model != None:
            self.data_model = model
        if graph != None:
            self.graph = graph

    def get_rdf_graph(self, schema : bool):
        """
        Generates an RDF graph based on the provided schema.
        This method creates an RDF graph by utilizing a data model and a semantic mapper.
        It sequentially builds the context model, collection model, and knowledge model
        to construct the final RDF graph.
        Args:
            schema (bool): A flag indicating whether to use the schema for mapping.
        Returns:
            rdflib.Graph: The generated RDF graph.
        """

        model = VEO2RDF(**self.data_model)
        mapper = VEORDFMapper(schema=schema)
        graphCon = mapper.get_context_model(mapper.veo_graph, model)
        graphCol = mapper.get_collection_model(graphCon, model)
        self.graph = mapper.get_knowledge_model(graphCol, model)
        return self.graph
    
    def get_neo4j_graph(self):
        """
        Retrieves the Neo4j graph instance.
        Returns:
            neo4j.GraphDatabase: The Neo4j graph instance associated with this object.
        """
        model = VEO2Cypher(**self.data_model)
        VEOCypherMapper(model)
        return None
    
    def save(self, name='populated-kg', output='ttl'):
        """
        Saves the current graph to a file in the specified format.
        Args:
            name (str): The name of the output file (default is 'populated-kg').
            output (str): The format of the output file, such as 'ttl' (default is 'ttl').
        Returns:
            None
        """

        graph_store(self.graph, name, output)

    def __str__(self):
        """
        Returns a string representation of the graph in Turtle format.
        This method serializes the graph object into a Turtle-formatted string,
        which is a compact and readable format for RDF data.
        Returns:
            str: The serialized graph in Turtle format.
        """

        return self.graph.serialize(format='turtle')
    
@staticmethod
def read_from_sac(path, ontology=False):
    """
    Reads data from a SAC file and generates an RDF graph.
    Args:
        path (str): The file path to the SAC file to be read.
        ontology (bool, optional): If True, includes ontology information in the RDF graph. Defaults to False.
    Returns:
        rdflib.Graph: An RDF graph generated from the SAC file.
    """
    data_model = SAC2VEO._parse_file(path)
    gm = GraphManager(data_model)
    graph = gm.get_rdf_graph(ontology)
    return graph

@staticmethod
def read_from_json(path, ontology=False):
    """
    Reads a JSON file and converts it into an RDF graph.
    
    Parameters:
        path: str
            The path to the JSON file.
        ontology: bool, optional
            If True, the graph will include ontology information. Defaults to False.      
    Returns:
        graph: rdflib.Graph
            The RDF graph created from the JSON data.
    """
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
